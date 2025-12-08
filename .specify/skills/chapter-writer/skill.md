# Chapter Writer Skill

Generate comprehensive MDX chapter content for the Physical AI & Humanoid Robotics textbook.

## Purpose

This skill consumes a chapter specification and produces complete MDX content suitable for the Docusaurus-based textbook platform. It generates educational content covering ROS2, Gazebo simulation, Unity integration, and humanoid robotics.

## Input Requirements

```json
{
  "chapter_id": "string",           // Unique identifier (e.g., "week-1-intro")
  "title": "string",                // Chapter title
  "module": "number",               // Module number (1-4)
  "week": "number",                 // Week number (1-13)
  "topic": "string",                // Main topic
  "description": "string",          // Brief description
  "prerequisites": ["string"],      // Required prior knowledge
  "learning_objectives": ["string"], // 4-6 specific objectives
  "key_concepts": ["string"],       // Core concepts to cover
  "lab_tasks": [{                   // Hands-on exercises
    "title": "string",
    "description": "string",
    "difficulty": "beginner|intermediate|advanced"
  }],
  "code_languages": ["python", "cpp", "bash"], // Languages for examples
  "estimated_duration": "string"    // e.g., "3 hours"
}
```

## Output Format

The skill outputs MDX content with the following structure:

```mdx
---
sidebar_position: {week}
title: "{title}"
description: "{description}"
---

import ChapterQuiz from '@site/src/components/ChapterQuiz';
import ChatSelection from '@site/src/components/ChatSelection';

# {title}

<ChatSelection chapterId="{chapter_id}">

## Learning Objectives

By the end of this chapter, you will be able to:

1. {objective_1}
2. {objective_2}
...

## Introduction

{engaging_introduction}

## Theory: {main_concept}

{theoretical_content_with_diagrams}

## Lab Tasks

### Task 1: {task_title}

{step_by_step_instructions}

```{language}
{code_example}
```

## Code Examples

{additional_code_examples}

## Summary

{key_takeaways}

## Additional Resources

- [Resource 1](url)
- [Resource 2](url)

</ChatSelection>

## Chapter Quiz

<ChapterQuiz chapterId="{chapter_id}" />
```

## Example Usage

### CLI
```bash
claude-code skill chapter-writer --input chapter-spec.json --output week-1-intro.mdx
```

### API
```python
from specify.skills import ChapterWriter

writer = ChapterWriter()
content = writer.generate({
    "chapter_id": "week-1-intro",
    "title": "Week 1: Introduction to ROS2",
    "module": 1,
    "week": 1,
    "topic": "ROS2 Fundamentals",
    "description": "Learn the fundamentals of ROS2 architecture",
    "prerequisites": [],
    "learning_objectives": [
        "Understand the core architecture of ROS2",
        "Set up a ROS2 development environment",
        "Create and run your first ROS2 node"
    ],
    "key_concepts": ["Nodes", "Topics", "DDS", "Packages"],
    "lab_tasks": [
        {
            "title": "Install ROS2 Humble",
            "description": "Set up ROS2 on Ubuntu 22.04",
            "difficulty": "beginner"
        }
    ],
    "code_languages": ["python", "cpp", "bash"],
    "estimated_duration": "3 hours"
})
```

## Content Guidelines

### Technical Accuracy
- Use ROS2 Humble as the reference distribution
- Reference Gazebo 11 (Classic) or Ignition Gazebo
- Unity examples use Unity 2022.x LTS
- All code must be tested and functional

### Pedagogical Structure
1. Start with motivation and real-world relevance
2. Build from simple to complex concepts
3. Provide multiple code examples (Python primary, C++ secondary)
4. Include common pitfalls and troubleshooting tips
5. End with practical exercises that reinforce learning

### Style Requirements
- Use active voice and second person ("you will")
- Include ASCII diagrams for architecture concepts
- Add Docusaurus admonitions (:::info, :::tip, :::caution)
- Link to official documentation where appropriate

## Integration

This skill integrates with:
- **summary** skill for generating key points
- **quiz-generator** skill for MCQ generation
- **validator** skill for consistency checking

## Dependencies

- Access to ROS2, Gazebo, Unity documentation
- Code execution environment for validation
- MDX parser for output verification
