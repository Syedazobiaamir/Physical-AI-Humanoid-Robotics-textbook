"""
Base Agent Class

Provides common functionality for all personalization agents including
profile-based adaptation, skill composition, and result formatting.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from ...utils.logger import logger


@dataclass
class UserProfile:
    """User profile for content personalization"""
    skill_level: str = "beginner"  # beginner, intermediate, advanced
    background: str = "neither"  # software, hardware, both, neither
    language_preference: str = "en"  # en, ur
    learning_goals: List[str] = None

    def __post_init__(self):
        if self.learning_goals is None:
            self.learning_goals = []


@dataclass
class AgentResult:
    """Standard result format for agent operations"""
    success: bool
    content: str
    original_content: str
    transformations_applied: List[str]
    metadata: Dict[str, Any]
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "content": self.content,
            "original_content": self.original_content,
            "transformations_applied": self.transformations_applied,
            "metadata": self.metadata,
            "error": self.error
        }


class BaseAgent(ABC):
    """
    Abstract base class for content personalization agents.

    Agents orchestrate one or more skills to transform content
    based on user profiles and specific use cases.
    """

    def __init__(self, name: str, description: str):
        """
        Initialize the agent.

        Args:
            name: Unique identifier for the agent
            description: Human-readable description of what the agent does
        """
        self.name = name
        self.description = description
        self.skills_used: List[str] = []

    @abstractmethod
    async def transform(
        self,
        content: str,
        profile: UserProfile,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Transform content based on user profile.

        Args:
            content: The content to transform
            profile: User profile for personalization
            context: Optional additional context (chapter info, etc.)

        Returns:
            AgentResult with transformed content and metadata
        """
        pass

    def _create_result(
        self,
        success: bool,
        content: str,
        original_content: str,
        transformations: List[str],
        metadata: Dict[str, Any] = None,
        error: str = None
    ) -> AgentResult:
        """Helper to create standardized results"""
        return AgentResult(
            success=success,
            content=content,
            original_content=original_content,
            transformations_applied=transformations,
            metadata=metadata or {},
            error=error
        )

    def _log_transformation(self, transformation: str, success: bool):
        """Log transformation for debugging and analytics"""
        status = "completed" if success else "failed"
        logger.info(f"Agent {self.name}: {transformation} {status}")

    async def can_handle(self, profile: UserProfile) -> bool:
        """
        Check if this agent is appropriate for the given profile.

        Override in subclasses for specific profile requirements.
        """
        return True

    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "skills_used": self.skills_used
        }
