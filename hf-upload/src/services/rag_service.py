"""
RAG (Retrieval-Augmented Generation) service for answering questions
"""
from typing import List, Optional, Dict, Any, Tuple
import time
from ..vector_store.qdrant_client import qdrant_store
from ..llm.provider import llm_provider
from ..utils.logger import logger


class RAGService:
    """
    Service for RAG-based question answering

    Uses vector search to retrieve relevant context and
    LLM to generate answers based on the retrieved content.
    """

    def __init__(self):
        """Initialize RAG service"""
        self.vector_store = qdrant_store
        self.llm = llm_provider

        # Default configuration
        self.top_k = 5
        self.score_threshold = 0.5  # Lowered from 0.7 for better recall
        self.max_context_tokens = 4000

    async def query(
        self,
        query: str,
        context_mode: str = "general",
        selected_text: Optional[str] = None,
        chapter_id: Optional[str] = None,
        use_anthropic_fallback: bool = True
    ) -> Dict[str, Any]:
        """
        Process a RAG query and return an answer

        Args:
            query: User's question
            context_mode: 'selection' for selected text context, 'general' for broad search
            selected_text: Text selected by user (if context_mode is 'selection')
            chapter_id: Optional chapter ID to filter results
            use_anthropic_fallback: Whether to use Anthropic if OpenAI fails

        Returns:
            Dictionary with answer, sources, and latency
        """
        start_time = time.time()

        try:
            # Step 1: Build search query
            search_query = self._build_search_query(query, selected_text, context_mode)

            # Step 2: Generate embedding for the query
            query_embedding = await self.llm.generate_embedding(search_query)

            if not query_embedding:
                return self._error_response("Failed to generate query embedding", start_time)

            # Step 3: Search for relevant context
            filter_conditions = {"chapter_id": chapter_id} if chapter_id else None

            search_results = self.vector_store.search(
                query_vector=query_embedding,
                limit=self.top_k,
                filter_conditions=filter_conditions,
                score_threshold=self.score_threshold
            )

            # Step 4: Extract context from results
            context_chunks, sources = self._extract_context(search_results)

            # Add selected text as additional context if provided
            if selected_text and context_mode == "selection":
                context_chunks.insert(0, f"Selected text: {selected_text}")

            # Step 5: Generate answer using LLM
            if context_chunks:
                answer = await self._generate_answer(
                    query=query,
                    context=context_chunks,
                    use_anthropic_fallback=use_anthropic_fallback
                )
            else:
                answer = await self._no_context_response(query)

            latency = time.time() - start_time

            return {
                "answer": answer,
                "sources": sources,
                "latency": round(latency, 3),
                "context_count": len(context_chunks),
                "model": "openai" if answer else "none"
            }

        except Exception as e:
            logger.error(f"RAG query error: {str(e)}")
            return self._error_response(str(e), start_time)

    def _build_search_query(
        self,
        query: str,
        selected_text: Optional[str],
        context_mode: str
    ) -> str:
        """Build optimized search query based on context mode"""
        if context_mode == "selection" and selected_text:
            # Combine selected text with query for more relevant search
            return f"{selected_text}\n\nQuestion: {query}"
        return query

    def _extract_context(
        self,
        search_results: List[Dict[str, Any]]
    ) -> Tuple[List[str], List[str]]:
        """
        Extract context chunks and source references from search results

        Returns:
            Tuple of (context_chunks, sources)
        """
        context_chunks = []
        sources = []

        for result in search_results:
            payload = result.get("payload", {})
            content = payload.get("content", "")
            chapter_id = payload.get("chapter_id", "")
            heading = payload.get("heading", "")

            if content:
                context_chunks.append(content)

                # Build source reference
                source = chapter_id
                if heading:
                    source = f"{chapter_id} - {heading}"
                if source and source not in sources:
                    sources.append(source)

        return context_chunks, sources

    async def _generate_answer(
        self,
        query: str,
        context: List[str],
        use_anthropic_fallback: bool = True
    ) -> str:
        """Generate answer using LLM (auto-selects best available provider)"""
        system_prompt = """You are a helpful AI teaching assistant for a Physical AI and Humanoid Robotics textbook.
Your role is to:
1. Answer questions accurately based on the provided context
2. Explain complex concepts in a clear, educational manner
3. Provide code examples when relevant
4. Reference specific sections when possible
5. If the context doesn't contain enough information, acknowledge this honestly

Format your responses clearly with proper markdown formatting for code blocks, lists, and emphasis."""

        try:
            answer = await self.llm.complete_with_context(
                query=query,
                context=context,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )

            if answer:
                return answer
        except Exception as e:
            logger.warning(f"LLM completion failed: {str(e)}")

        return "I apologize, but I'm unable to generate a response at this time. Please try again later."

    async def _no_context_response(self, query: str) -> str:
        """Generate response when no relevant context is found - use LLM directly"""
        # Use Gemini directly for general questions when no context is found
        system_prompt = """You are a helpful AI teaching assistant for a Physical AI and Humanoid Robotics textbook.
You are an expert in robotics, ROS2, computer vision, motion planning, control systems, and humanoid robotics.

Since no specific textbook content was found for this question, provide a helpful educational response based on your knowledge.
Format your response with clear explanations and include code examples where relevant.
Use markdown formatting for better readability."""

        try:
            response = await self.llm.complete(
                prompt=f"Question: {query}\n\nProvide a helpful, educational response:",
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            if response:
                return response
        except Exception as e:
            logger.warning(f"Fallback LLM completion failed: {e}")

        return f"""I couldn't find specific information in the textbook content related to your question: "{query}"

Here are some suggestions:
1. Try rephrasing your question with different keywords
2. Check the chapter index to find the relevant section
3. Select specific text in the chapter and ask about that content

If you're looking for general information, I'd recommend reviewing the learning objectives at the beginning of each chapter."""

    def _error_response(self, error_message: str, start_time: float) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "answer": f"An error occurred while processing your question. Please try again. Error: {error_message}",
            "sources": [],
            "latency": round(time.time() - start_time, 3),
            "context_count": 0,
            "model": "error"
        }

    async def get_health(self) -> Dict[str, Any]:
        """
        Check health status of RAG components

        Returns:
            Health status dictionary
        """
        available_providers = self.llm.get_available_providers()

        health = {
            "status": "healthy",
            "components": {
                "vector_store": False,
                "llm": len(available_providers) > 0
            },
            "providers": available_providers
        }

        # Check vector store
        try:
            info = self.vector_store.get_collection_info()
            if info:
                health["components"]["vector_store"] = True
                health["vector_count"] = info.get("vectors_count", 0)
        except Exception as e:
            logger.error(f"Vector store health check failed: {str(e)}")

        # Test embedding generation
        if available_providers:
            try:
                test_embedding = await self.llm.generate_embedding("test")
                if test_embedding:
                    health["embedding_working"] = True
            except Exception as e:
                logger.error(f"Embedding health check failed: {str(e)}")
                health["embedding_working"] = False

        # Overall status
        if not health["components"]["llm"]:
            health["status"] = "unhealthy"
        elif not health["components"]["vector_store"]:
            health["status"] = "degraded"

        return health


# Singleton instance
rag_service = RAGService()
