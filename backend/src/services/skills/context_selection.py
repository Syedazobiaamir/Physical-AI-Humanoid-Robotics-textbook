"""
Context Selection Skill

This skill provides focused RAG-based Q&A for user-selected text passages.
It answers questions specifically about the selected content, providing
deeper understanding and clarification of specific concepts.
"""

from typing import Optional, Dict, Any, List
from ...llm.provider import llm_provider
from ...vector_store.qdrant_client import qdrant_store
from ...utils.logger import logger


CONTEXT_SELECTION_PROMPT = """You are an expert AI teaching assistant for a Physical AI and Humanoid Robotics textbook.
The user has selected specific text and is asking a question about it.

Selected Text:
---
{selected_text}
---

{additional_context}

User's Question: {question}

Instructions:
1. Focus your answer specifically on the selected text
2. Explain any technical concepts mentioned in the selection
3. Provide concrete examples when helpful
4. If the question asks about something not in the selection, acknowledge this and provide what you can
5. Use clear, educational language appropriate for the user's level
6. Include relevant code examples if the selected text contains code

Provide a clear, focused answer:"""


CONTEXT_EXPANSION_PROMPT = """Based on this selected text from a robotics textbook, identify related concepts
that would provide additional context. Return only the key terms, separated by commas.

Selected text: {selected_text}

Related concepts:"""


async def context_selection(
    question: str,
    selected_text: str,
    chapter_id: Optional[str] = None,
    expand_context: bool = True,
    user_level: str = "intermediate"
) -> Dict[str, Any]:
    """
    Answer questions about user-selected text with focused context.

    This skill provides targeted Q&A for specific text passages, allowing users
    to get deeper understanding of particular concepts they've highlighted.

    Args:
        question: The user's question about the selected text
        selected_text: The text the user has selected/highlighted
        chapter_id: Optional chapter ID for additional context filtering
        expand_context: Whether to search for related content to enhance the answer
        user_level: User's knowledge level (beginner, intermediate, advanced)

    Returns:
        dict with:
            - answer: The response to the user's question
            - selected_text: Echo of the selected text
            - related_concepts: List of related concepts found
            - sources: List of source references used
            - success: Boolean indicating if the skill succeeded
    """
    try:
        if not selected_text or not selected_text.strip():
            return {
                "answer": "Please select some text from the chapter to ask questions about.",
                "selected_text": "",
                "related_concepts": [],
                "sources": [],
                "success": False,
                "error": "No text selected"
            }

        if not question or not question.strip():
            return {
                "answer": "Please provide a question about the selected text.",
                "selected_text": selected_text,
                "related_concepts": [],
                "sources": [],
                "success": False,
                "error": "No question provided"
            }

        # Step 1: Get additional context if enabled
        additional_context_text = ""
        related_concepts = []
        sources = []

        if expand_context:
            context_data = await _expand_context(
                selected_text=selected_text,
                question=question,
                chapter_id=chapter_id
            )
            additional_context_text = context_data.get("context_text", "")
            related_concepts = context_data.get("concepts", [])
            sources = context_data.get("sources", [])

        # Step 2: Build the prompt with appropriate level
        level_instruction = _get_level_instruction(user_level)

        additional_context = ""
        if additional_context_text:
            additional_context = f"""
Additional Context from the textbook:
---
{additional_context_text}
---
"""

        prompt = CONTEXT_SELECTION_PROMPT.format(
            selected_text=selected_text,
            additional_context=additional_context,
            question=question
        )

        # Step 3: Generate the answer
        result = await llm_provider.complete(
            prompt=prompt,
            system_prompt=f"You are a knowledgeable robotics instructor. {level_instruction}",
            temperature=0.7,
            max_tokens=1500
        )

        if not result:
            return {
                "answer": "I couldn't generate a response. Please try again.",
                "selected_text": selected_text,
                "related_concepts": related_concepts,
                "sources": sources,
                "success": False,
                "error": "LLM returned empty response"
            }

        return {
            "answer": result,
            "selected_text": selected_text,
            "related_concepts": related_concepts,
            "sources": sources,
            "context_expanded": expand_context and bool(additional_context_text),
            "success": True
        }

    except Exception as e:
        logger.error(f"Error in context_selection skill: {str(e)}")
        return {
            "answer": f"An error occurred while processing your question: {str(e)}",
            "selected_text": selected_text,
            "related_concepts": [],
            "sources": [],
            "success": False,
            "error": str(e)
        }


async def _expand_context(
    selected_text: str,
    question: str,
    chapter_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Expand context by searching for related content in the vector store.

    Args:
        selected_text: The selected text to find related content for
        question: The user's question
        chapter_id: Optional chapter filter

    Returns:
        dict with context_text, concepts, and sources
    """
    try:
        # Build combined query from selection and question
        search_query = f"{selected_text}\n\nQuestion: {question}"

        # Generate embedding for search
        query_embedding = await llm_provider.generate_embedding(search_query)

        if not query_embedding:
            return {"context_text": "", "concepts": [], "sources": []}

        # Search for related content
        filter_conditions = {"chapter_id": chapter_id} if chapter_id else None

        search_results = qdrant_store.search(
            query_vector=query_embedding,
            limit=3,  # Limit to top 3 for focused context
            filter_conditions=filter_conditions,
            score_threshold=0.5
        )

        # Extract context and sources
        context_chunks = []
        sources = []
        concepts = []

        for result in search_results:
            payload = result.get("payload", {})
            content = payload.get("content", "")
            chapter = payload.get("chapter_id", "")
            heading = payload.get("heading", "")

            if content and content not in selected_text:  # Avoid duplicating selected text
                context_chunks.append(content)

                source = f"{chapter} - {heading}" if heading else chapter
                if source and source not in sources:
                    sources.append(source)

        # Extract key concepts (simple keyword extraction)
        concepts = await _extract_concepts(selected_text)

        return {
            "context_text": "\n\n".join(context_chunks[:3]),
            "concepts": concepts,
            "sources": sources
        }

    except Exception as e:
        logger.warning(f"Context expansion failed: {str(e)}")
        return {"context_text": "", "concepts": [], "sources": []}


async def _extract_concepts(text: str) -> List[str]:
    """
    Extract key concepts from the selected text.

    Args:
        text: Text to extract concepts from

    Returns:
        List of key concept strings
    """
    try:
        result = await llm_provider.complete(
            prompt=CONTEXT_EXPANSION_PROMPT.format(selected_text=text[:500]),
            system_prompt="Extract only the main technical concepts. Return them as a comma-separated list.",
            temperature=0.3,
            max_tokens=100
        )

        if result:
            concepts = [c.strip() for c in result.split(",")]
            return concepts[:5]  # Limit to top 5 concepts

    except Exception as e:
        logger.warning(f"Concept extraction failed: {str(e)}")

    return []


def _get_level_instruction(level: str) -> str:
    """Get instruction modifier based on user level."""
    instructions = {
        "beginner": "Use simple language and provide analogies. Define all technical terms.",
        "intermediate": "Use clear technical language. Explain complex concepts when needed.",
        "advanced": "Use precise technical terminology. Focus on implementation details."
    }
    return instructions.get(level, instructions["intermediate"])
