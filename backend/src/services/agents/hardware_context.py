"""
Hardware Context Agent

Enhances content with hardware implementation details for users
with hardware/electronics backgrounds.
"""

from typing import Dict, Any, Optional
from .base import BaseAgent, UserProfile, AgentResult
from ..skills.hardware_mapping import hardware_mapping
from ..skills.real_world_robot_example import real_world_robot_example
from ...utils.logger import logger


class HardwareContextAgent(BaseAgent):
    """
    Agent that adds hardware context and implementation details.

    Best suited for users with hardware/electronics backgrounds
    who want to understand the physical implementation of robotics concepts.
    """

    def __init__(self):
        super().__init__(
            name="hardware_context",
            description="Adds hardware implementation details and real-world robot examples"
        )
        self.skills_used = ["hardware_mapping", "real_world_robot_example"]

    async def transform(
        self,
        content: str,
        profile: UserProfile,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Transform content by adding hardware context.

        Args:
            content: Original content to enhance
            profile: User profile for customization
            context: Optional context (chapter info, etc.)

        Returns:
            AgentResult with hardware-enhanced content
        """
        transformations = []
        metadata = {
            "profile_background": profile.background,
            "profile_level": profile.skill_level
        }

        try:
            # Determine detail level based on profile
            if profile.skill_level == "beginner":
                detail_level = "basic"
            elif profile.skill_level == "advanced":
                detail_level = "advanced"
            else:
                detail_level = "intermediate"

            # Step 1: Add hardware mapping
            self._log_transformation("hardware_mapping", True)
            hw_result = await hardware_mapping(
                content=content,
                detail_level=detail_level
            )

            if hw_result["success"]:
                transformations.append("hardware_mapping")
                metadata["hardware_refs"] = hw_result.get("hardware_refs", [])
                metadata["protocols"] = hw_result.get("protocols_mentioned", [])
                enhanced_content = hw_result["enhanced"]
            else:
                enhanced_content = content

            # Step 2: Add real-world robot examples
            self._log_transformation("real_world_robot_example", True)
            robot_result = await real_world_robot_example(
                content=enhanced_content,
                ros_only=True  # Focus on ROS-compatible robots
            )

            if robot_result["success"]:
                transformations.append("real_world_robot_example")
                metadata["robots_mentioned"] = robot_result.get("robots_mentioned", [])
                metadata["try_it_suggestions"] = robot_result.get("try_it_suggestions", [])
                final_content = robot_result["enhanced"]
            else:
                final_content = enhanced_content

            return self._create_result(
                success=True,
                content=final_content,
                original_content=content,
                transformations=transformations,
                metadata=metadata
            )

        except Exception as e:
            logger.error(f"HardwareContextAgent error: {str(e)}")
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

        Best for users with hardware backgrounds.
        """
        return profile.background in ["hardware", "both"]
