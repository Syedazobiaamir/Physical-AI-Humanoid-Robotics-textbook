"""
Simplify for Beginner Skill

This skill transforms technical content into beginner-friendly explanations
with analogies, simplified terminology, and step-by-step breakdowns.
"""

from typing import Optional
from ...llm.provider import llm_provider
from ...utils.logger import logger


SIMPLIFY_PROMPT = """You are an expert robotics educator. Transform the following technical content
into a beginner-friendly explanation. Your goal is to make complex robotics concepts accessible
to someone with no prior experience.

Guidelines:
1. Use everyday analogies (e.g., "A ROS node is like a worker in a factory")
2. Replace jargon with simple terms, but mention the technical term in parentheses
3. Break down complex processes into numbered steps
4. Add "Why this matters" explanations
5. Include a "Key Takeaway" at the end
6. Keep code examples but add detailed comments explaining each line
7. Use bullet points for lists of concepts
8. Add helpful emojis sparingly for visual cues

Original Content:
{content}

Simplified version for beginners:"""


async def simplify_for_beginner(
    content: str,
    context: Optional[str] = None,
    preserve_code: bool = True
) -> dict:
    """
    Transform technical content into beginner-friendly explanations.

    Args:
        content: The technical content to simplify
        context: Optional context about the chapter or topic
        preserve_code: If True, keep code blocks but add explanatory comments

    Returns:
        dict with:
            - simplified: The simplified content
            - analogies_used: List of analogies introduced
            - terms_explained: List of technical terms that were explained
            - success: Boolean indicating if transformation succeeded
    """
    try:
        prompt = SIMPLIFY_PROMPT.format(content=content)

        if context:
            prompt = f"Context: {context}\n\n{prompt}"

        if not preserve_code:
            prompt += "\n\nNote: You may simplify or remove code examples if they're too complex."

        result = await llm_provider.complete(
            prompt=prompt,
            system_prompt="You are a friendly robotics teacher who excels at explaining complex concepts simply.",
            temperature=0.7,
            max_tokens=2000
        )

        if not result:
            return {
                "simplified": content,
                "analogies_used": [],
                "terms_explained": [],
                "success": False,
                "error": "LLM returned empty response"
            }

        # Extract analogies and terms (basic extraction)
        analogies = []
        terms = []

        # Look for common analogy patterns
        if "like a" in result.lower() or "similar to" in result.lower():
            # Simple heuristic - in production, use more sophisticated extraction
            analogies.append("analogy_detected")

        # Look for parenthetical technical terms
        import re
        term_matches = re.findall(r'\(([A-Za-z\s]+)\)', result)
        terms = [t.strip() for t in term_matches if len(t) < 50]

        return {
            "simplified": result,
            "analogies_used": analogies,
            "terms_explained": terms[:10],  # Limit to top 10
            "success": True
        }

    except Exception as e:
        logger.error(f"Error in simplify_for_beginner: {str(e)}")
        return {
            "simplified": content,
            "analogies_used": [],
            "terms_explained": [],
            "success": False,
            "error": str(e)
        }
