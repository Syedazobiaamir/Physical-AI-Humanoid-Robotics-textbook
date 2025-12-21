"""
Embodied Intelligence Agent

Focuses on the intersection of AI and physical systems,
emphasizing how intelligence emerges from embodiment.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAgent, UserProfile, AgentResult
from ...llm.provider import llm_provider
from ...utils.logger import logger


class EmbodiedIntelligenceAgent(BaseAgent):
    """
    Agent specializing in embodied AI concepts.

    Enhances content with:
    - Physical-cognitive connections
    - Sensor-action loops
    - Morphological computation
    - Real-world grounding
    """

    # Key concepts in embodied intelligence
    EMBODIMENT_CONCEPTS = [
        "sensor-action coupling",
        "morphological computation",
        "physical grounding",
        "situated cognition",
        "enactivism",
        "affordances",
        "embodied simulation",
        "predictive processing",
    ]

    def __init__(self):
        super().__init__(
            name="embodied_intelligence",
            description="Emphasizes embodied cognition and physical-AI connections"
        )
        self.skills_used = ["embodiment_analysis", "physical_grounding"]

    async def transform(
        self,
        content: str,
        profile: UserProfile,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """
        Transform content with embodied intelligence perspective.

        Args:
            content: Original content
            profile: User profile
            context: Optional context

        Returns:
            AgentResult with embodiment-enhanced content
        """
        transformations = []
        metadata = {
            "profile_level": profile.skill_level,
            "embodiment_concepts": []
        }

        try:
            # Analyze content for embodiment opportunities
            relevant_concepts = self._find_relevant_concepts(content)
            metadata["embodiment_concepts"] = relevant_concepts

            # Build enhancement prompt
            prompt = self._build_embodiment_prompt(content, profile, relevant_concepts)

            result = await llm_provider.complete(
                prompt=prompt,
                system_prompt=self._get_system_prompt(),
                temperature=0.7,
                max_tokens=2500
            )

            if result:
                transformations.append("embodiment_enhancement")

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
            logger.error(f"EmbodiedIntelligenceAgent error: {str(e)}")
            return self._create_result(
                success=False,
                content=content,
                original_content=content,
                transformations=transformations,
                metadata=metadata,
                error=str(e)
            )

    def _get_system_prompt(self) -> str:
        """System prompt for embodied intelligence perspective"""
        return """You are an expert in embodied cognition and physical AI.
You understand that intelligence in robots emerges from the interaction
between the agent's body, brain, and environment - not just computation.

Your explanations always:
1. Emphasize the physical body's role in cognition
2. Discuss sensor-motor loops and feedback systems
3. Explain how morphology (body shape) influences behavior
4. Connect software concepts to physical implementation
5. Reference biological systems as inspiration

Key principles you teach:
- "The body is not just a vehicle for the brain"
- "Intelligence is shaped by physical interaction"
- "Perception and action are deeply coupled"
- "The environment is part of the cognitive system"
"""

    def _find_relevant_concepts(self, content: str) -> List[str]:
        """Find which embodiment concepts are relevant to the content"""
        content_lower = content.lower()
        relevant = []

        # Keywords that suggest embodiment opportunities
        keyword_map = {
            "sensor": ["sensor-action coupling", "physical grounding"],
            "motor": ["sensor-action coupling", "morphological computation"],
            "perception": ["situated cognition", "affordances"],
            "control": ["predictive processing", "sensor-action coupling"],
            "navigation": ["embodied simulation", "physical grounding"],
            "manipulation": ["affordances", "morphological computation"],
            "learning": ["enactivism", "embodied simulation"],
            "vision": ["situated cognition", "affordances"],
        }

        for keyword, concepts in keyword_map.items():
            if keyword in content_lower:
                relevant.extend(concepts)

        return list(set(relevant))

    def _build_embodiment_prompt(
        self,
        content: str,
        profile: UserProfile,
        concepts: List[str]
    ) -> str:
        """Build the embodiment enhancement prompt"""
        level_guidance = {
            "beginner": "Use simple analogies to biological systems (humans, animals)",
            "intermediate": "Include technical details of sensor-motor integration",
            "advanced": "Discuss theoretical frameworks like enactivism and predictive processing"
        }

        prompt = f"""Enhance this robotics content with an embodied intelligence perspective.

Relevant embodiment concepts to incorporate: {', '.join(concepts) if concepts else 'general embodiment principles'}

Guidance for this student level: {level_guidance.get(profile.skill_level, level_guidance['intermediate'])}

Add these elements:
1. **Embodiment Insight**: How the physical body shapes this capability
2. **Biological Parallel**: How animals or humans solve similar problems
3. **Sensor-Motor Connection**: How perception and action work together here
4. **Design Implication**: How understanding embodiment improves robot design

Original Content:
{content}

Content enhanced with embodied intelligence perspective:"""

        return prompt

    async def can_handle(self, profile: UserProfile) -> bool:
        """
        This agent is best for intermediate and advanced users
        or those interested in AI/cognitive aspects.
        """
        if "ai" in [g.lower() for g in profile.learning_goals]:
            return True
        return profile.skill_level in ["intermediate", "advanced"]
