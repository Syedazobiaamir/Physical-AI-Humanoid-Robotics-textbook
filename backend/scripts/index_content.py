#!/usr/bin/env python3
"""
Content Indexing Script for Physical AI & Humanoid Robotics Textbook

This script indexes all chapter content from the frontend/docs directory
into the Qdrant vector database for RAG-powered chat functionality.

Usage:
    python scripts/index_content.py [--force] [--chapter CHAPTER_ID]

Arguments:
    --force: Force reindex all content, even if unchanged
    --chapter: Index only a specific chapter (e.g., "week-1-intro")
"""

import asyncio
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv()

from database.base import AsyncSessionLocal, init_db
from services.indexing_service import IndexingService
from utils.logger import logger


# Path to docs directory (relative to this script)
DOCS_PATH = Path(__file__).parent.parent.parent / "frontend" / "docs"


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from MDX content"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1].strip()
            body = parts[2].strip()

            # Simple YAML parsing for title
            frontmatter = {}
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")

            return frontmatter, body

    return {}, content


def get_chapter_files() -> List[Dict[str, Any]]:
    """Get all MDX/MD chapter files from docs directory"""
    chapters = []

    if not DOCS_PATH.exists():
        logger.error(f"Docs path does not exist: {DOCS_PATH}")
        return chapters

    # Walk through all docs
    for file_path in DOCS_PATH.rglob("*.mdx"):
        relative_path = file_path.relative_to(DOCS_PATH)
        chapter_id = relative_path.stem  # e.g., "week-1-intro"

        try:
            content = file_path.read_text(encoding="utf-8")
            frontmatter, body = extract_frontmatter(content)

            # Generate title from frontmatter or filename
            title = frontmatter.get("title", chapter_id.replace("-", " ").title())

            chapters.append({
                "id": chapter_id,
                "title": title,
                "content": body,
                "path": str(relative_path),
                "module": relative_path.parent.name if relative_path.parent.name != "docs" else "intro"
            })

            logger.info(f"Found chapter: {chapter_id} - {title}")

        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")

    # Also check for .md files
    for file_path in DOCS_PATH.rglob("*.md"):
        if file_path.suffix == ".md":
            relative_path = file_path.relative_to(DOCS_PATH)
            chapter_id = relative_path.stem

            try:
                content = file_path.read_text(encoding="utf-8")
                frontmatter, body = extract_frontmatter(content)
                title = frontmatter.get("title", chapter_id.replace("-", " ").title())

                chapters.append({
                    "id": chapter_id,
                    "title": title,
                    "content": body,
                    "path": str(relative_path),
                    "module": relative_path.parent.name if relative_path.parent.name != "docs" else "intro"
                })

                logger.info(f"Found chapter: {chapter_id} - {title}")

            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")

    return chapters


async def index_chapters(
    chapters: List[Dict[str, Any]],
    force: bool = False,
    chapter_filter: str = None
) -> Dict[str, Any]:
    """Index chapters into vector database"""

    # Filter chapters if specific one requested
    if chapter_filter:
        chapters = [c for c in chapters if c["id"] == chapter_filter]
        if not chapters:
            logger.error(f"Chapter not found: {chapter_filter}")
            return {"status": "error", "message": f"Chapter not found: {chapter_filter}"}

    # Initialize database
    await init_db()

    async with AsyncSessionLocal() as db:
        indexing_service = IndexingService(db)

        results = await indexing_service.index_all_chapters(
            chapters=chapters,
            force_reindex=force
        )

        return results


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Index chapter content into vector database"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force reindex all content"
    )
    parser.add_argument(
        "--chapter", "-c",
        type=str,
        help="Index only a specific chapter ID"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available chapters without indexing"
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("Physical AI Textbook - Content Indexing")
    print("=" * 60 + "\n")

    # Get chapters
    chapters = get_chapter_files()

    if not chapters:
        print("No chapters found!")
        return

    print(f"Found {len(chapters)} chapters:\n")
    for ch in chapters:
        print(f"  - [{ch['module']}] {ch['id']}: {ch['title']}")

    if args.list:
        return

    print("\n" + "-" * 60)
    print("Starting indexing...\n")

    # Check for required environment variables
    if not os.getenv("QDRANT_URL") and not os.getenv("QDRANT_API_KEY"):
        print("WARNING: Qdrant not configured. Using local SQLite only.")
        print("Set QDRANT_URL and QDRANT_API_KEY for vector search.\n")

    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        print("ERROR: No AI API key configured!")
        print("Set OPENAI_API_KEY or GEMINI_API_KEY for embeddings.")
        return

    # Run indexing
    results = await index_chapters(
        chapters=chapters,
        force=args.force,
        chapter_filter=args.chapter
    )

    # Print results
    print("\n" + "=" * 60)
    print("Indexing Results")
    print("=" * 60 + "\n")

    print(f"  Total chapters: {results.get('total', 0)}")
    print(f"  Successfully indexed: {results.get('success', 0)}")
    print(f"  Skipped (unchanged): {results.get('skipped', 0)}")
    print(f"  Errors: {results.get('errors', 0)}")

    if results.get('details'):
        print("\nDetails:")
        for detail in results['details']:
            status_icon = "✓" if detail['status'] == 'success' else "○" if detail['status'] == 'skipped' else "✗"
            chunks = detail.get('chunk_count', 0)
            print(f"  {status_icon} {detail['chapter_id']}: {detail['status']} ({chunks} chunks)")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
