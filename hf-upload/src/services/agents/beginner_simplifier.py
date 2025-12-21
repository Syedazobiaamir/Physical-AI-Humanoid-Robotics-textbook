"""
Beginner Simplifier Agent

Transforms complex robotics content into beginner-friendly explanations
with analogies, simplified terminology, and step-by-step breakdowns.
"""

from typing import Dict, Any, Optional
from .base import BaseAgent, UserProfile, AgentResult
from ..skills.simplify_for_beginner import simplify_for_beginner
from ..skills.exam_ready_summary import exam_ready_summary
from ...utils.logger import logger


class BeginnerSimplifierAgent(BaseAgent):
    """
    Agent that simplifies content for beginners.

    Uses analogies, simple language, and step-by-step explanations
    to make complex robotics concepts accessible to newcomers.
    """

    def __init__(self):
        super().__init__(
            name="beginner_simplifier",
            description="Simplifies technical content for beginners with analogies and clear explanations"
        )
        self.skills_used = ["simplify_for_beginner", "exam_ready_summary"]

    async def transform(
        self,
        content: str,
        profile: UserProfile,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Transform content into beginner-friendly format.

        Args:
            content: Original technical content
            profile: User profile for customization
            context: Optional context (chapter info, etc.)

        Returns:
            AgentResult with simplified content
        """
        transformations = []
        metadata = {
            "profile_level": profile.skill_level,
            "profile_background": profile.background
        }

        try:
            # Get chapter context if available
            chapter_context = None
            if context:
                chapter_context = context.get("chapter_title", context.get("chapter_id"))

            # Step 1: Simplify the content
            self._log_transformation("simplify_for_beginner", True)
            simplify_result = await simplify_for_beginner(
                content=content,
                context=chapter_context,
                preserve_code=True  # Keep code but add explanatory comments
            )

            if simplify_result["success"]:
                transformations.append("simplify_for_beginner")
                metadata["analogies_used"] = simplify_result.get("analogies_used", [])
                metadata["terms_explained"] = simplify_result.get("terms_explained", [])
                simplified_content = simplify_result["simplified"]
            else:
                simplified_content = content

            # Step 2: Add a study summary for beginners
            # Only if content is substantial
            if len(content) > 500:
                self._log_transformation("exam_ready_summary", True)
                summary_result = await exam_ready_summary(
                    content=simplified_content,
                    difficulty="basic",
                    include_practice_questions=True
                )

                if summary_result["success"]:
                    transformations.append("exam_ready_summary")
                    metadata["key_concepts"] = summary_result.get("key_concepts", [])
                    metadata["practice_questions"] = summary_result.get("practice_questions", [])

                    # Append summary as a "Study Guide" section
                    final_content = simplified_content + "\n\n---\n\n## Study Guide\n\n" + summary_result["summary"]
                else:
                    final_content = simplified_content
            else:
                final_content = simplified_content

            return self._create_result(
                success=True,
                content=final_content,
                original_content=content,
                transformations=transformations,
                metadata=metadata
            )

        except Exception as e:
            logger.error(f"BeginnerSimplifierAgent error: {str(e)}")
            return self._create_result(
                success=False,
                content=content,
                original_content=content,
                transformations=transformations,
                metadata=metadata,
                error=str(e)
            )

    async def can_handle(self, profile: UserProfile) -> bool:
        """
        Check if this agent is appropriate for the profile.

        Best for beginner users.
        """
        return profile.skill_level == "beginner"
