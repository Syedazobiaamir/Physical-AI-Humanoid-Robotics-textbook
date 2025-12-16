# Subagent Reuse Patterns

This document describes the reusable AI skills and subagent architecture used in the Physical AI Textbook Platform. This architecture earns hackathon bonus points (50 pts) for demonstrating Claude Code skills and subagent composition patterns.

## Overview

The platform implements a two-tier AI architecture:

1. **Skills** - Focused, single-purpose functions that perform specific content transformations
2. **Subagents** - Orchestrators that compose multiple skills based on user context

This separation enables:
- **Reusability**: Skills can be invoked independently or composed
- **Testability**: Each skill can be tested in isolation
- **Extensibility**: New skills can be added without modifying existing agents
- **Composability**: Agents can mix and match skills for different use cases

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        API ENDPOINTS                                 │
│  POST /api/personalize  │  POST /api/rag/query  │  POST /api/translate │
└───────────────┬─────────────────┬─────────────────────┬─────────────┘
                │                 │                     │
                ▼                 ▼                     ▼
┌───────────────────────────────────────────────────────────────────┐
│                         SUBAGENTS                                   │
│  ┌───────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │ Personalization   │  │ Context         │  │ Translation      │  │
│  │ Agent             │  │ Selection Agent │  │ Agent            │  │
│  │                   │  │                 │  │                  │  │
│  │ Orchestrates:     │  │ Uses:           │  │ Uses:            │  │
│  │ - Strategy select │  │ - RAG pipeline  │  │ - Gemini API     │  │
│  │ - Skill dispatch  │  │ - Vector search │  │ - RTL formatting │  │
│  └───────────────────┘  └─────────────────┘  └──────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
                │                 │                     │
                ▼                 ▼                     ▼
┌───────────────────────────────────────────────────────────────────┐
│                           SKILLS                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │ simplify_for_   │  │ hardware_       │  │ context_        │    │
│  │ beginner        │  │ mapping         │  │ selection       │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │ exam_ready_     │  │ real_world_     │  │ translation     │    │
│  │ summary         │  │ robot_example   │  │ (Urdu)          │    │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘    │
└───────────────────────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────────┐
│                     LLM PROVIDER (Gemini API)                       │
└───────────────────────────────────────────────────────────────────┘
```

---

## Skills Reference

### 1. `simplify_for_beginner`

**Purpose**: Transforms technical content into beginner-friendly explanations.

**Location**: `backend/src/services/skills/simplify_for_beginner.py`

**Interface**:
```python
async def simplify_for_beginner(
    content: str,
    context: Optional[str] = None,
    preserve_code: bool = True
) -> dict:
    """
    Returns:
        simplified: The simplified content
        analogies_used: List of analogies introduced
        terms_explained: List of technical terms explained
        success: Boolean
    """
```

**Example Usage**:
```python
from backend.src.services.skills import simplify_for_beginner

result = await simplify_for_beginner(
    content="ROS2 uses DDS for inter-process communication...",
    context="Chapter 3: Robot Operating System",
    preserve_code=True
)

if result["success"]:
    print(result["simplified"])
```

---

### 2. `context_selection`

**Purpose**: Provides focused Q&A for user-selected text passages.

**Location**: `backend/src/services/skills/context_selection.py`

**Interface**:
```python
async def context_selection(
    question: str,
    selected_text: str,
    chapter_id: Optional[str] = None,
    expand_context: bool = True,
    user_level: str = "intermediate"
) -> dict:
    """
    Returns:
        answer: Response to the question
        selected_text: Echo of selected text
        related_concepts: List of related concepts
        sources: List of source references
        success: Boolean
    """
```

**Example Usage**:
```python
from backend.src.services.skills import context_selection

result = await context_selection(
    question="What is forward kinematics?",
    selected_text="Forward kinematics computes end-effector position...",
    chapter_id="module-2/kinematics",
    user_level="beginner"
)
```

---

### 3. `hardware_mapping`

**Purpose**: Maps software concepts to hardware implementations.

**Location**: `backend/src/services/skills/hardware_mapping.py`

**Use Case**: For users with strong hardware background, enhances content with physical component references.

---

### 4. `exam_ready_summary`

**Purpose**: Generates study summaries with key concepts and practice questions.

**Location**: `backend/src/services/skills/exam_ready_summary.py`

**Use Case**: Creates "Study Guide" sections for chapters.

---

### 5. `real_world_robot_example`

**Purpose**: Adds real-world robot examples to abstract concepts.

**Location**: `backend/src/services/skills/real_world_robot_example.py`

**Use Case**: References actual robots (Boston Dynamics Spot, Tesla Optimus) for concepts.

---

## Subagents Reference

### PersonalizationAgent

**Purpose**: Orchestrates personalization based on user profile.

**Location**: `backend/src/agents/personalization_agent.py`

**Strategy Selection Logic**:
```python
def _select_strategy(self, profile: PersonalizationProfile) -> str:
    if profile.is_beginner:
        return "beginner"        # Uses simplify_for_beginner
    elif profile.is_hardware_focused:
        return "hardware_focused" # Uses hardware_mapping
    elif profile.is_advanced:
        return "advanced"        # Adds technical depth
    else:
        return "default"         # Light adaptation
```

**Example Usage**:
```python
from backend.src.agents import personalization_agent, PersonalizationProfile

profile = PersonalizationProfile(
    software_level="beginner",
    hardware_exposure="none",
    robotics_experience="none"
)

result = await personalization_agent.personalize(
    content="Original chapter content...",
    profile=profile,
    context={"chapter_id": "module-1/intro"}
)

if result.success:
    adapted_content = result.content
    print(f"Applied: {result.adaptations_applied}")
```

---

### TranslationAgent

**Purpose**: Translates content to Urdu with RTL formatting.

**Location**: `backend/src/agents/translation_skill.py`

**Features**:
- Uses Gemini API for high-quality translation
- Preserves code blocks in LTR
- Adds RTL CSS classes

---

### QuizGeneratorAgent

**Purpose**: Generates assessment questions from chapter content.

**Location**: `backend/src/agents/quiz_generator.py`

**Features**:
- Creates multiple choice and short answer questions
- Difficulty based on user profile
- Tied to specific learning objectives

---

## Composing Skills in New Agents

To create a new agent that composes existing skills:

```python
from backend.src.services.agents.base import BaseAgent, UserProfile, AgentResult
from backend.src.services.skills import simplify_for_beginner, hardware_mapping

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="custom_agent",
            description="Custom content transformation"
        )
        self.skills_used = ["simplify_for_beginner", "hardware_mapping"]

    async def transform(
        self,
        content: str,
        profile: UserProfile,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        transformations = []

        # Step 1: Simplify if needed
        if profile.skill_level == "beginner":
            result = await simplify_for_beginner(content)
            if result["success"]:
                content = result["simplified"]
                transformations.append("simplify_for_beginner")

        # Step 2: Add hardware context if appropriate
        if profile.background in ("hardware", "both"):
            result = await hardware_mapping(content)
            if result["success"]:
                content = result["enhanced"]
                transformations.append("hardware_mapping")

        return self._create_result(
            success=True,
            content=content,
            original_content=original,
            transformations=transformations,
            metadata={}
        )
```

---

## Benefits of This Architecture

### 1. Single Responsibility
Each skill does one thing well. This makes debugging easier and allows focused testing.

### 2. Open/Closed Principle
New skills can be added without modifying existing agents. Agents can adopt new skills by updating their skill list.

### 3. Dependency Inversion
Agents depend on skill interfaces, not implementations. Skills can be swapped or mocked for testing.

### 4. Reusability Across Endpoints
The same skill can be used by multiple endpoints:
- `/api/personalize` uses `simplify_for_beginner`
- `/api/rag/query` uses `context_selection`
- Both could use `hardware_mapping` in the future

### 5. Composability for Complex Workflows
Agents can chain skills sequentially or in parallel:
```python
# Sequential composition
simplified = await simplify_for_beginner(content)
with_hardware = await hardware_mapping(simplified["content"])
final = await exam_ready_summary(with_hardware["content"])
```

---

## Testing Skills and Agents

### Unit Testing a Skill
```python
import pytest
from backend.src.services.skills import simplify_for_beginner

@pytest.mark.asyncio
async def test_simplify_for_beginner():
    result = await simplify_for_beginner(
        content="ROS2 nodes communicate via topics...",
        context="ROS chapter"
    )

    assert result["success"] is True
    assert len(result["simplified"]) > 0
    assert "analogy" in result["simplified"].lower() or result["analogies_used"]
```

### Integration Testing an Agent
```python
import pytest
from backend.src.agents import personalization_agent, PersonalizationProfile

@pytest.mark.asyncio
async def test_personalization_agent_beginner():
    profile = PersonalizationProfile(software_level="beginner")

    result = await personalization_agent.personalize(
        content="Complex robotics content...",
        profile=profile
    )

    assert result.success is True
    assert "beginner_simplification" in result.adaptations_applied
```

---

## Hackathon Bonus Points (50 pts)

This architecture demonstrates:

1. **Modular AI Skills**: 5+ reusable skills with clear interfaces
2. **Subagent Composition**: Agents that orchestrate multiple skills
3. **Profile-Based Adaptation**: Dynamic skill selection based on user attributes
4. **Testable Design**: Each component can be tested independently
5. **Documentation**: Clear patterns for extension and reuse

The key innovation is treating AI capabilities as composable building blocks rather than monolithic functions, enabling rapid development of new personalization features by mixing existing skills.
