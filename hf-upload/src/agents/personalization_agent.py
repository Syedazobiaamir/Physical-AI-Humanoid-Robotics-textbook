"""
Personalization Agent (Subagent)

A reusable subagent that orchestrates multiple skills to personalize content
based on user profile attributes including skill level, background, and preferences.

This agent can be composed into larger workflows and demonstrates the
Skills + Subagents pattern for the hackathon bonus points.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from ..utils.logger import logger
from ..llm.provider import llm_provider


@dataclass
class PersonalizationProfile:
    """User profile for content personalization"""
    software_level: str = "beginner"  # beginner, intermediate, advanced
    hardware_exposure: str = "none"  # none, some, extensive
    robotics_experience: str = "none"  # none, some, extensive
    language_preference: str = "en"  # en, ur
    learning_goals: List[str] = None

    def __post_init__(self):
        if self.learning_goals is None:
            self.learning_goals = []

    @property
    def is_beginner(self) -> bool:
        """Check if user is a beginner across all dimensions"""
        return (
            self.software_level == "beginner" and
            self.hardware_exposure in ("none", "some") and
            self.robotics_experience in ("none", "some")
        )

    @property
    def is_hardware_focused(self) -> bool:
        """Check if user has strong hardware background"""
        return self.hardware_exposure == "extensive"

    @property
    def is_advanced(self) -> bool:
        """Check if user is advanced"""
        return (
            self.software_level == "advanced" or
            self.robotics_experience == "extensive"
        )


@dataclass
class PersonalizationResult:
    """Result of personalization transformation"""
    success: bool
    content: str
    original_content: str
    adaptations_applied: List[str]
    metadata: Dict[str, Any]
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "content": self.content,
            "original_content": self.original_content,
            "adaptations_applied": self.adaptations_applied,
            "metadata": self.metadata,
            "error": self.error
        }


# Prompt templates for different personalization strategies
BEGINNER_PROMPT = """You are a patient robotics educator. Transform the following content
to be more accessible for beginners. Your transformations should:

1. Replace jargon with simpler terms (keep technical terms in parentheses)
2. Add helpful analogies comparing robotics concepts to everyday experiences
3. Break down complex processes into numbered steps
4. Explain WHY each concept matters
5. Add a "Key Takeaway" at the end
6. Keep code examples but add detailed comments

Original Content:
{content}

Beginner-Friendly Version:"""


HARDWARE_FOCUSED_PROMPT = """You are a robotics educator with strong hardware expertise.
Transform the following content to emphasize hardware aspects and physical implementations.

Your transformations should:
1. Highlight connections to physical components (sensors, actuators, controllers)
2. Add real-world hardware examples (specific robot models, components)
3. Include practical considerations (power, wiring, mounting)
4. Connect software concepts to their hardware counterparts
5. Reference common development boards (Raspberry Pi, Arduino, Jetson)

Original Content:
{content}

Hardware-Enhanced Version:"""


ADVANCED_PROMPT = """You are an expert robotics researcher. Transform the following content
to provide deeper technical insights for advanced practitioners.

Your transformations should:
1. Add technical precision and formal terminology
2. Include references to academic concepts and research areas
3. Discuss edge cases and failure modes
4. Add optimization considerations
5. Connect to state-of-the-art techniques

Original Content:
{content}

Advanced Technical Version:"""


class PersonalizationAgent:
    """
    Reusable Personalization Subagent

    Orchestrates personalization skills based on user profile to adapt
    textbook content for different learning needs.

    This agent is designed to be:
    - Reusable: Can be invoked from any endpoint or workflow
    - Composable: Can be combined with other agents
    - Profile-Aware: Adapts strategy based on user attributes
    """

    def __init__(self):
        """Initialize the personalization agent"""
        self.name = "personalization_agent"
        self.description = "Adapts textbook content based on user profile"
        self.llm = llm_provider

    async def personalize(
        self,
        content: str,
        profile: PersonalizationProfile,
        context: Optional[Dict[str, Any]] = None
    ) -> PersonalizationResult:
        """
        Personalize content based on user profile.

        This is the main entry point for the subagent. It analyzes the
        user profile and selects appropriate personalization strategies.

        Args:
            content: The original content to personalize
            profile: User profile with background information
            context: Optional context (chapter_id, topic, etc.)

        Returns:
            PersonalizationResult with adapted content
        """
        adaptations = []
        metadata = {
            "profile": {
                "software_level": profile.software_level,
                "hardware_exposure": profile.hardware_exposure,
                "robotics_experience": profile.robotics_experience,
                "language_preference": profile.language_preference
            }
        }

        try:
            # Determine personalization strategy based on profile
            strategy = self._select_strategy(profile)
            metadata["strategy"] = strategy

            # Apply the appropriate transformation
            if strategy == "beginner":
                result = await self._apply_beginner_adaptation(content, profile, context)
                adaptations.append("beginner_simplification")

            elif strategy == "hardware_focused":
                result = await self._apply_hardware_adaptation(content, profile, context)
                adaptations.append("hardware_enhancement")

            elif strategy == "advanced":
                result = await self._apply_advanced_adaptation(content, profile, context)
                adaptations.append("advanced_deepening")

            else:
                # Default: minimal adaptation
                result = await self._apply_light_adaptation(content, profile, context)
                adaptations.append("light_adaptation")

            if result:
                return PersonalizationResult(
                    success=True,
                    content=result,
                    original_content=content,
                    adaptations_applied=adaptations,
                    metadata=metadata
                )
            else:
                # If LLM fails, return original with note
                return PersonalizationResult(
                    success=False,
                    content=content,
                    original_content=content,
                    adaptations_applied=[],
                    metadata=metadata,
                    error="Personalization service unavailable"
                )

        except Exception as e:
            logger.error(f"PersonalizationAgent error: {str(e)}")
            return PersonalizationResult(
                success=False,
                content=content,
                original_content=content,
                adaptations_applied=adaptations,
                metadata=metadata,
                error=str(e)
            )

    def _select_strategy(self, profile: PersonalizationProfile) -> str:
        """
        Select personalization strategy based on profile.

        Strategy priority:
        1. Beginner users get simplified content
        2. Hardware-focused users get hardware-enhanced content
        3. Advanced users get deeper technical content
        4. Others get light adaptation
        """
        if profile.is_beginner:
            return "beginner"
        elif profile.is_hardware_focused:
            return "hardware_focused"
        elif profile.is_advanced:
            return "advanced"
        else:
            return "default"

    async def _apply_beginner_adaptation(
        self,
        content: str,
        profile: PersonalizationProfile,
        context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """Apply beginner-friendly adaptations"""
        prompt = BEGINNER_PROMPT.format(content=content[:4000])  # Limit input size

        result = await self.llm.complete(
            prompt=prompt,
            system_prompt="You are a friendly robotics teacher who makes complex concepts simple.",
            temperature=0.7,
            max_tokens=2500
        )

        return result

    async def _apply_hardware_adaptation(
        self,
        content: str,
        profile: PersonalizationProfile,
        context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """Apply hardware-focused adaptations"""
        prompt = HARDWARE_FOCUSED_PROMPT.format(content=content[:4000])

        result = await self.llm.complete(
            prompt=prompt,
            system_prompt="You are a robotics hardware expert who connects software to physical implementation.",
            temperature=0.7,
            max_tokens=2500
        )

        return result

    async def _apply_advanced_adaptation(
        self,
        content: str,
        profile: PersonalizationProfile,
        context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """Apply advanced technical adaptations"""
        prompt = ADVANCED_PROMPT.format(content=content[:4000])

        result = await self.llm.complete(
            prompt=prompt,
            system_prompt="You are a robotics researcher providing deep technical insights.",
            temperature=0.7,
            max_tokens=2500
        )

        return result

    async def _apply_light_adaptation(
        self,
        content: str,
        profile: PersonalizationProfile,
        context: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        """Apply minimal adaptations for intermediate users"""
        # For intermediate users, just add helpful notes
        prompt = f"""Add helpful clarifications to this robotics content where appropriate.
Keep the original structure and depth, but:
1. Add brief explanations for any assumed knowledge
2. Highlight practical applications

Content:
{content[:4000]}

Enhanced version:"""

        result = await self.llm.complete(
            prompt=prompt,
            system_prompt="You are a helpful robotics instructor.",
            temperature=0.5,
            max_tokens=2500
        )

        return result

    def get_info(self) -> Dict[str, Any]:
        """Get agent information for debugging/monitoring"""
        return {
            "name": self.name,
            "description": self.description,
            "strategies": ["beginner", "hardware_focused", "advanced", "default"]
        }


# Singleton instance for easy import
personalization_agent = PersonalizationAgent()
