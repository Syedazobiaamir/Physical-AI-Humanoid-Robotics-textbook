"""
Exam Ready Summary Skill

This skill creates concise, exam-focused summaries with key points,
common exam questions, and memory aids for studying.
"""

from typing import Optional, List
from ...llm.provider import llm_provider
from ...utils.logger import logger


SUMMARY_PROMPT = """You are an expert robotics educator preparing students for exams.
Create an exam-ready summary of the following content.

Include:
1. **Key Concepts** - Bullet points of the most important ideas (5-10 points)
2. **Definitions to Remember** - Technical terms and their concise definitions
3. **Common Exam Questions** - 5 likely exam questions with brief answers
4. **Memory Aids** - Mnemonics or memory tricks for complex concepts
5. **Quick Reference** - Formulas, commands, or syntax to memorize
6. **Common Mistakes** - What students often get wrong

Format the summary for quick review (use headers, bullets, bold for key terms).

Original Content:
{content}

Exam-Ready Summary:"""


async def exam_ready_summary(
    content: str,
    focus_areas: Optional[List[str]] = None,
    include_practice_questions: bool = True,
    difficulty: str = "intermediate"
) -> dict:
    """
    Create an exam-focused summary with key points and practice questions.

    Args:
        content: The content to summarize
        focus_areas: Specific topics to emphasize
        include_practice_questions: Whether to include practice exam questions
        difficulty: "basic", "intermediate", or "advanced"

    Returns:
        dict with:
            - summary: The exam-ready summary
            - key_concepts: List of key concepts identified
            - practice_questions: List of practice questions
            - definitions: Dictionary of terms and definitions
            - success: Boolean indicating success
    """
    try:
        prompt = SUMMARY_PROMPT.format(content=content)

        if focus_areas:
            prompt += f"\n\nPay special attention to these topics: {', '.join(focus_areas)}"

        if not include_practice_questions:
            prompt = prompt.replace("**Common Exam Questions**", "").replace("5 likely exam questions with brief answers", "")

        if difficulty == "basic":
            prompt += "\n\nKeep the summary simple, focusing on foundational concepts."
        elif difficulty == "advanced":
            prompt += "\n\nInclude advanced topics, edge cases, and tricky exam scenarios."

        result = await llm_provider.complete(
            prompt=prompt,
            system_prompt="You are an experienced robotics professor who has written many exams.",
            temperature=0.5,  # Lower temperature for more focused output
            max_tokens=2000
        )

        if not result:
            return {
                "summary": "",
                "key_concepts": [],
                "practice_questions": [],
                "definitions": {},
                "success": False,
                "error": "LLM returned empty response"
            }

        # Extract key concepts (look for bullet points after "Key Concepts")
        key_concepts = []
        definitions = {}
        practice_questions = []

        lines = result.split('\n')
        current_section = ""

        for line in lines:
            line = line.strip()

            # Detect sections
            if "key concept" in line.lower():
                current_section = "concepts"
            elif "definition" in line.lower():
                current_section = "definitions"
            elif "exam question" in line.lower() or "practice question" in line.lower():
                current_section = "questions"
            elif line.startswith("- ") or line.startswith("* ") or line.startswith("• "):
                content = line[2:].strip()

                if current_section == "concepts" and len(content) > 5:
                    key_concepts.append(content[:200])  # Limit length
                elif current_section == "definitions" and ":" in content:
                    parts = content.split(":", 1)
                    if len(parts) == 2:
                        definitions[parts[0].strip()] = parts[1].strip()
                elif current_section == "questions" and len(content) > 10:
                    practice_questions.append(content[:300])

        return {
            "summary": result,
            "key_concepts": key_concepts[:15],  # Limit to top 15
            "practice_questions": practice_questions[:10],  # Limit to 10
            "definitions": dict(list(definitions.items())[:20]),  # Limit to 20
            "success": True
        }

    except Exception as e:
        logger.error(f"Error in exam_ready_summary: {str(e)}")
        return {
            "summary": "",
            "key_concepts": [],
            "practice_questions": [],
            "definitions": {},
            "success": False,
            "error": str(e)
        }
