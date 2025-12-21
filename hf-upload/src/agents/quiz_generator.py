"""
Claude Code subagent for generating chapter quizzes

This agent can be invoked via:
    claude-code run-subagent quiz-generator \
        --input '{"text": "Chapter text here"}' \
        --output docs/module-1/ros2-fundamentals-quiz.json
"""
from typing import Dict, Any, List
import json
from ..llm.openai_client import openai_client
from ..llm.anthropic_client import anthropic_client
from ..utils.logger import logger


class QuizGeneratorAgent:
    """
    Agent for generating 5 multiple-choice questions from chapter content
    """

    def __init__(self):
        """Initialize the quiz generator agent"""
        self.openai = openai_client
        self.anthropic = anthropic_client

    async def generate_quiz(self, chapter_text: str, chapter_id: str = None) -> Dict[str, Any]:
        """
        Generate a quiz with 5 MCQs from chapter content

        Args:
            chapter_text: Full text of the chapter
            chapter_id: Optional chapter identifier

        Returns:
            Quiz data structure with questions, options, and correct answers
        """
        logger.info(f"Generating quiz for chapter: {chapter_id or 'unknown'}")

        # Build the generation prompt
        system_prompt = """You are an expert at creating educational assessments.
Generate exactly 5 multiple-choice questions based on the provided chapter content.

Each question must:
1. Test understanding of key concepts
2. Have 4 distinct answer options
3. Have one clearly correct answer
4. Include a brief explanation of why the correct answer is right

Return the quiz as a JSON object with this structure:
{
  "questions": [
    {
      "id": "q1",
      "text": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Explanation of correct answer"
    }
  ]
}

Use 0-based indexing for correct_answer (0 = first option, 1 = second option, etc.)."""

        prompt = f"""Generate a 5-question multiple-choice quiz based on this chapter content:

{chapter_text[:3000]}

Create questions that:
- Cover different sections of the chapter
- Range from basic recall to application/analysis
- Are clear and unambiguous
- Have plausible distractors

Return ONLY the JSON object, no additional text."""

        try:
            # Try OpenAI first
            quiz_json = await self.openai.complete(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2000
            )

            if quiz_json:
                # Parse and validate JSON
                quiz_data = self._parse_and_validate_quiz(quiz_json, chapter_id)
                if quiz_data:
                    logger.info(f"Successfully generated quiz with OpenAI")
                    return quiz_data

            # Fallback to Anthropic
            logger.warning("OpenAI failed, falling back to Anthropic Claude")
            quiz_json = await self.anthropic.complete(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2000
            )

            if quiz_json:
                quiz_data = self._parse_and_validate_quiz(quiz_json, chapter_id)
                if quiz_data:
                    logger.info(f"Successfully generated quiz with Claude")
                    return quiz_data

            logger.error("Both OpenAI and Claude failed to generate quiz")
            return self._generate_fallback_quiz(chapter_id)

        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            return self._generate_fallback_quiz(chapter_id)

    def _parse_and_validate_quiz(self, quiz_json: str, chapter_id: str = None) -> Dict[str, Any]:
        """Parse and validate quiz JSON"""
        try:
            # Extract JSON from response (in case there's extra text)
            start = quiz_json.find('{')
            end = quiz_json.rfind('}') + 1
            if start >= 0 and end > start:
                quiz_json = quiz_json[start:end]

            quiz_data = json.loads(quiz_json)

            # Validate structure
            if "questions" not in quiz_data:
                logger.error("Quiz JSON missing 'questions' field")
                return None

            questions = quiz_data["questions"]
            if len(questions) != 5:
                logger.warning(f"Quiz has {len(questions)} questions instead of 5")

            # Validate each question
            for i, q in enumerate(questions):
                if not all(key in q for key in ["id", "text", "options", "correct_answer"]):
                    logger.error(f"Question {i} missing required fields")
                    return None
                if len(q["options"]) != 4:
                    logger.error(f"Question {i} has {len(q['options'])} options instead of 4")
                    return None

            # Add chapter_id if provided
            if chapter_id:
                quiz_data["chapter_id"] = chapter_id

            return quiz_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse quiz JSON: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error validating quiz: {str(e)}")
            return None

    def _generate_fallback_quiz(self, chapter_id: str = None) -> Dict[str, Any]:
        """Generate a basic fallback quiz template"""
        return {
            "chapter_id": chapter_id or "unknown",
            "questions": [
                {
                    "id": f"q{i+1}",
                    "text": f"Sample question {i+1}?",
                    "options": [
                        "Option A",
                        "Option B",
                        "Option C",
                        "Option D"
                    ],
                    "correct_answer": 0,
                    "explanation": "Explanation to be added"
                }
                for i in range(5)
            ]
        }


# Singleton instance
quiz_generator = QuizGeneratorAgent()
