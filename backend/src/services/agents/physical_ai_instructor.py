"""
Physical AI Instructor Agent

An expert robotics instructor agent that provides comprehensive
guidance on physical AI and embodied systems.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAgent, UserProfile, AgentResult
from ...llm.provider import llm_provider
from ...utils.logger import logger


class PhysicalAIInstructor(BaseAgent):
    """
    Expert instructor agent for Physical AI concepts.

    Provides:
    - Curriculum-aligned explanations
    - Hands-on project suggestions
    - Industry connections
    - Career guidance
    """

    def __init__(self):
        super().__init__(
            name="physical_ai_instructor",
            description="Expert Physical AI instructor providing curriculum guidance and industry insights"
        )
        self.skills_used = ["curriculum_alignment", "project_suggestion", "industry_connection"]

    async def transform(
        self,
        content: str,
        profile: UserProfile,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Transform content with expert instructor perspective.

        Args:
            content: Original content
            profile: User profile
            context: Optional context

        Returns:
            AgentResult with instructor-enhanced content
        """
        transformations = []
        metadata = {
            "profile_level": profile.skill_level,
            "learning_goals": profile.learning_goals
        }

        try:
            # Build instructor prompt based on profile
            instructor_prompt = self._build_instructor_prompt(content, profile, context)

            result = await llm_provider.complete(
                prompt=instructor_prompt,
                system_prompt=self._get_system_prompt(profile),
                temperature=0.7,
                max_tokens=2500
            )

            if result:
                transformations.append("instructor_enhancement")
                metadata["sections_added"] = self._detect_sections(result)

                return self._create_result(
                    success=True,
                    content=result,
                    original_content=content,
                    transformations=transformations,
                    metadata=metadata
                )
            else:
                return self._create_result(
                    success=False,
                    content=content,
                    original_content=content,
                    transformations=[],
                    metadata=metadata,
                    error="LLM returned empty response"
                )

        except Exception as e:
            logger.error(f"PhysicalAIInstructor error: {str(e)}")
            return self._create_result(
                success=False,
                content=content,
                original_content=content,
                transformations=transformations,
                metadata=metadata,
                error=str(e)
            )

    def _get_system_prompt(self, profile: UserProfile) -> str:
        """Generate system prompt based on user profile"""
        level_context = {
            "beginner": "patient and encouraging, using simple explanations",
            "intermediate": "technical but accessible, building on existing knowledge",
            "advanced": "expert-level, discussing nuances and edge cases"
        }

        return f"""You are Dr. Alex Chen, a distinguished professor of Robotics and AI with 20 years
of experience in both academia and industry. You've worked at Boston Dynamics, NVIDIA, and now
lead the Physical AI research lab at a top university.

Your teaching style is {level_context.get(profile.skill_level, level_context['intermediate'])}.

You always:
1. Connect theory to practical applications
2. Share real industry experiences and examples
3. Suggest hands-on projects appropriate for the student's level
4. Point out common mistakes and how to avoid them
5. Encourage questions and exploration"""

    def _build_instructor_prompt(
        self,
        content: str,
        profile: UserProfile,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Build the instructor transformation prompt"""
        prompt = f"""As an expert Physical AI instructor, enhance the following content for a student.

Student Profile:
- Level: {profile.skill_level}
- Background: {profile.background}
- Goals: {', '.join(profile.learning_goals) if profile.learning_goals else 'General learning'}

Add these sections to the content:
1. **Instructor's Note**: A brief personal insight about why this topic matters
2. **Industry Connection**: How this is used in real companies/projects
3. **Hands-On Challenge**: A practical project or exercise
4. **Common Pitfalls**: What students often get wrong
5. **Going Further**: Resources and next steps for motivated students

Original Content:
{content}

Enhanced content with instructor perspective:"""

        return prompt

    def _detect_sections(self, content: str) -> List[str]:
        """Detect which sections were added"""
        sections = []
        if "Instructor's Note" in content or "instructor's note" in content.lower():
            sections.append("instructor_note")
        if "Industry Connection" in content or "industry" in content.lower():
            sections.append("industry_connection")
        if "Hands-On" in content or "hands-on" in content.lower():
            sections.append("hands_on_challenge")
        if "Common Pitfall" in content or "pitfall" in content.lower():
            sections.append("common_pitfalls")
        if "Going Further" in content or "next steps" in content.lower():
            sections.append("going_further")
        return sections

    async def can_handle(self, profile: UserProfile) -> bool:
        """This agent can handle all profiles"""
        return True
