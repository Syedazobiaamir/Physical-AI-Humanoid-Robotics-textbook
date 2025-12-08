"""
Indexing service for processing and storing chapter content in vector database
"""
from typing import List, Dict, Any, Optional
import re
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models.vector_chunk import VectorChunk
from ..vector_store.qdrant_client import qdrant_store
from ..llm.openai_client import openai_client
from ..utils.logger import logger


class IndexingService:
    """
    Service for indexing textbook content into the vector database

    Handles:
    - Text chunking with overlap
    - Embedding generation
    - Vector store upserts
    - Incremental updates
    """

    def __init__(self, db: AsyncSession):
        """Initialize indexing service"""
        self.db = db
        self.vector_store = qdrant_store
        self.openai = openai_client

        # Chunking configuration
        self.chunk_size = 500  # tokens
        self.chunk_overlap = 50  # tokens
        self.max_batch_size = 20  # embeddings per batch

    async def index_chapter(
        self,
        chapter_id: str,
        content: str,
        title: str,
        force_reindex: bool = False
    ) -> Dict[str, Any]:
        """
        Index a chapter's content

        Args:
            chapter_id: Chapter identifier
            content: Full chapter content (MDX/Markdown)
            title: Chapter title
            force_reindex: If True, delete existing chunks and reindex

        Returns:
            Indexing result with statistics
        """
        try:
            # Calculate content hash for change detection
            content_hash = self._calculate_hash(content)

            # Check if reindexing is needed
            if not force_reindex:
                existing = await self._get_existing_chunks(chapter_id)
                if existing and len(existing) > 0:
                    # Check if content has changed
                    existing_hash = self._calculate_hash(
                        "".join([c.content for c in existing])
                    )
                    if existing_hash == content_hash:
                        logger.info(f"Chapter {chapter_id} is up to date, skipping indexing")
                        return {
                            "status": "skipped",
                            "chapter_id": chapter_id,
                            "reason": "content_unchanged",
                            "chunk_count": len(existing)
                        }

            # Delete existing chunks if reindexing
            await self._delete_chapter_chunks(chapter_id)

            # Parse and chunk content
            chunks = self._chunk_content(content, title, chapter_id)

            if not chunks:
                logger.warning(f"No chunks generated for chapter {chapter_id}")
                return {
                    "status": "empty",
                    "chapter_id": chapter_id,
                    "chunk_count": 0
                }

            # Generate embeddings in batches
            embeddings = await self._generate_embeddings_batch(
                [c["content"] for c in chunks]
            )

            if len(embeddings) != len(chunks):
                logger.error(f"Embedding count mismatch for chapter {chapter_id}")
                return {
                    "status": "error",
                    "chapter_id": chapter_id,
                    "error": "embedding_count_mismatch"
                }

            # Store chunks in database and vector store
            stored_count = await self._store_chunks(chunks, embeddings, chapter_id)

            logger.info(f"Indexed chapter {chapter_id}: {stored_count} chunks")

            return {
                "status": "success",
                "chapter_id": chapter_id,
                "chunk_count": stored_count,
                "content_hash": content_hash
            }

        except Exception as e:
            logger.error(f"Error indexing chapter {chapter_id}: {str(e)}")
            return {
                "status": "error",
                "chapter_id": chapter_id,
                "error": str(e)
            }

    def _chunk_content(
        self,
        content: str,
        title: str,
        chapter_id: str
    ) -> List[Dict[str, Any]]:
        """
        Split content into chunks with metadata

        Args:
            content: Full content text
            title: Document title
            chapter_id: Chapter identifier

        Returns:
            List of chunk dictionaries
        """
        chunks = []

        # Clean and normalize content
        cleaned = self._clean_content(content)

        # Split by sections (headings)
        sections = self._split_by_sections(cleaned)

        chunk_index = 0
        for section in sections:
            heading = section.get("heading", "")
            text = section.get("text", "")

            if not text.strip():
                continue

            # Further split large sections
            section_chunks = self._split_text(text, self.chunk_size, self.chunk_overlap)

            for chunk_text in section_chunks:
                if len(chunk_text.strip()) < 50:  # Skip very small chunks
                    continue

                chunks.append({
                    "content": chunk_text,
                    "heading": heading,
                    "chapter_id": chapter_id,
                    "doc_id": f"{chapter_id}-{chunk_index}",
                    "chunk_index": chunk_index,
                    "title": title
                })
                chunk_index += 1

        return chunks

    def _clean_content(self, content: str) -> str:
        """Clean and normalize content"""
        # Remove import statements
        content = re.sub(r'^import\s+.*$', '', content, flags=re.MULTILINE)

        # Remove component tags but keep content
        content = re.sub(r'<ChapterQuiz[^>]*/?>', '', content)
        content = re.sub(r'<ChatSelection[^>]*>', '', content)
        content = re.sub(r'</ChatSelection>', '', content)

        # Keep code blocks content
        # content = re.sub(r'```[\s\S]*?```', '', content)  # Keep code for context

        # Remove HTML comments
        content = re.sub(r'<!--[\s\S]*?-->', '', content)

        # Normalize whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)

        return content.strip()

    def _split_by_sections(self, content: str) -> List[Dict[str, str]]:
        """Split content by markdown headings"""
        sections = []

        # Split by headings (## or ###)
        pattern = r'^(#{2,3})\s+(.+)$'
        lines = content.split('\n')

        current_section = {"heading": "", "text": ""}

        for line in lines:
            match = re.match(pattern, line)
            if match:
                # Save current section
                if current_section["text"].strip():
                    sections.append(current_section)

                # Start new section
                current_section = {
                    "heading": match.group(2).strip(),
                    "text": ""
                }
            else:
                current_section["text"] += line + "\n"

        # Add last section
        if current_section["text"].strip():
            sections.append(current_section)

        return sections

    def _split_text(
        self,
        text: str,
        chunk_size: int,
        overlap: int
    ) -> List[str]:
        """Split text into overlapping chunks"""
        # Simple word-based chunking
        words = text.split()

        if len(words) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)

            # Move forward with overlap
            start = end - overlap
            if start >= len(words):
                break

        return chunks

    async def _generate_embeddings_batch(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """Generate embeddings in batches"""
        all_embeddings = []

        for i in range(0, len(texts), self.max_batch_size):
            batch = texts[i:i + self.max_batch_size]
            embeddings = await self.openai.generate_embeddings_batch(batch)
            all_embeddings.extend(embeddings)

        return all_embeddings

    async def _store_chunks(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]],
        chapter_id: str
    ) -> int:
        """Store chunks in database and vector store"""
        stored_count = 0

        for chunk, embedding in zip(chunks, embeddings):
            try:
                # Create database record
                vector_chunk = VectorChunk(
                    doc_id=chunk["doc_id"],
                    chapter_id=chunk["chapter_id"],
                    heading=chunk["heading"],
                    chunk_index=chunk["chunk_index"],
                    content=chunk["content"],
                    token_count=len(chunk["content"].split())
                )

                self.db.add(vector_chunk)
                await self.db.flush()

                # Store in vector database
                self.vector_store.upsert_vectors(
                    vectors=[embedding],
                    payloads=[vector_chunk.to_payload()],
                    ids=[vector_chunk.id]
                )

                # Update embedding_id reference
                vector_chunk.embedding_id = vector_chunk.id
                stored_count += 1

            except Exception as e:
                logger.error(f"Error storing chunk {chunk['doc_id']}: {str(e)}")

        await self.db.commit()
        return stored_count

    async def _get_existing_chunks(self, chapter_id: str) -> List[VectorChunk]:
        """Get existing chunks for a chapter"""
        result = await self.db.execute(
            select(VectorChunk).where(VectorChunk.chapter_id == chapter_id)
        )
        return list(result.scalars().all())

    async def _delete_chapter_chunks(self, chapter_id: str) -> bool:
        """Delete all chunks for a chapter"""
        try:
            # Delete from vector store
            self.vector_store.delete_by_filter({"chapter_id": chapter_id})

            # Delete from database
            await self.db.execute(
                delete(VectorChunk).where(VectorChunk.chapter_id == chapter_id)
            )
            await self.db.commit()

            logger.info(f"Deleted existing chunks for chapter {chapter_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting chunks for chapter {chapter_id}: {str(e)}")
            await self.db.rollback()
            return False

    def _calculate_hash(self, content: str) -> str:
        """Calculate hash of content for change detection"""
        return hashlib.md5(content.encode()).hexdigest()

    async def index_all_chapters(
        self,
        chapters: List[Dict[str, Any]],
        force_reindex: bool = False
    ) -> Dict[str, Any]:
        """
        Index multiple chapters

        Args:
            chapters: List of chapter dictionaries with id, content, title
            force_reindex: If True, reindex all chapters

        Returns:
            Summary of indexing results
        """
        results = {
            "total": len(chapters),
            "success": 0,
            "skipped": 0,
            "errors": 0,
            "details": []
        }

        for chapter in chapters:
            result = await self.index_chapter(
                chapter_id=chapter["id"],
                content=chapter["content"],
                title=chapter["title"],
                force_reindex=force_reindex
            )

            results["details"].append(result)

            if result["status"] == "success":
                results["success"] += 1
            elif result["status"] == "skipped":
                results["skipped"] += 1
            else:
                results["errors"] += 1

        return results

    async def update_chapter_incremental(
        self,
        chapter_id: str,
        content: str,
        title: str
    ) -> Dict[str, Any]:
        """
        Incrementally update a chapter's index

        Only updates if content has changed.

        Args:
            chapter_id: Chapter identifier
            content: Updated content
            title: Chapter title

        Returns:
            Update result
        """
        return await self.index_chapter(
            chapter_id=chapter_id,
            content=content,
            title=title,
            force_reindex=False
        )
