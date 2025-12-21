"""
Claude Code subagent for generating full MDX chapters

This agent can be invoked via:
    claude-code run-subagent chapter-writer \
        --input '{"chapter": "Module 1 - ROS2 Fundamentals"}' \
        --output docs/module-1/ros2-fundamentals.mdx
"""
from typing import Dict, Any
import json
from ..llm.openai_client import openai_client
from ..llm.anthropic_client import anthropic_client
from ..utils.logger import logger


class ChapterWriterAgent:
    """
    Agent for generating complete textbook chapters in MDX format
    """

    def __init__(self):
        """Initialize the chapter writer agent"""
        self.openai = openai_client
        self.anthropic = anthropic_client

    async def generate_chapter(self, chapter_info: Dict[str, Any]) -> str:
        """
        Generate a complete chapter with learning objectives, theory, lab tasks, and code examples

        Args:
            chapter_info: Dictionary containing chapter metadata
                - chapter: Chapter title (e.g., "Module 1 - ROS2 Fundamentals")
                - module: Module number (e.g., "Module 1")
                - week: Week number (e.g., 1)
                - topics: List of topics to cover

        Returns:
            MDX content for the chapter
        """
        chapter_title = chapter_info.get("chapter", "Untitled Chapter")
        module = chapter_info.get("module", "Module 1")
        week = chapter_info.get("week", 1)
        topics = chapter_info.get("topics", [])

        logger.info(f"Generating chapter: {chapter_title}")

        # Build the generation prompt
        system_prompt = """You are an expert technical writer specializing in robotics and AI education.
Generate a comprehensive textbook chapter in MDX format suitable for a university-level course on Physical AI and Humanoid Robotics.

The chapter must include:
1. Frontmatter with metadata
2. Learning objectives (3-5 clear, measurable objectives)
3. Introduction and motivation
4. Theoretical content with clear explanations
5. Code examples with syntax highlighting
6. Lab tasks and exercises
7. Summary and key takeaways
8. References and further reading

Use proper MDX syntax, code blocks with language tags, and clear section headings."""

        prompt = f"""Generate a complete chapter for: {chapter_title}

Module: {module}
Week: {week}
Topics to cover: {', '.join(topics) if topics else 'Cover all fundamental topics for this chapter'}

Format the chapter in MDX with:
- Frontmatter (YAML) with sidebar_position, title, description
- Clear section headings (## for main sections)
- Code examples in appropriate languages (Python, C++, YAML, etc.)
- Practical exercises and lab tasks
- Visual aids descriptions (diagrams, charts)

Make it engaging, technically accurate, and suitable for students learning robotics."""

        try:
            # Try OpenAI first
            chapter_content = await self.openai.complete(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            if chapter_content:
                logger.info(f"Successfully generated chapter with OpenAI: {chapter_title}")
                return chapter_content

            # Fallback to Anthropic
            logger.warning("OpenAI failed, falling back to Anthropic Claude")
            chapter_content = await self.anthropic.complete(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=4000
            )

            if chapter_content:
                logger.info(f"Successfully generated chapter with Claude: {chapter_title}")
                return chapter_content

            logger.error("Both OpenAI and Claude failed to generate chapter")
            return self._generate_fallback_chapter(chapter_info)

        except Exception as e:
            logger.error(f"Error generating chapter: {str(e)}")
            return self._generate_fallback_chapter(chapter_info)

    def _generate_fallback_chapter(self, chapter_info: Dict[str, Any]) -> str:
        """Generate a basic fallback chapter template"""
        chapter_title = chapter_info.get("chapter", "Untitled Chapter")
        week = chapter_info.get("week", 1)

        return f"""---
sidebar_position: {week}
title: {chapter_title}
description: Chapter content for {chapter_title}
---

# {chapter_title}

## Learning Objectives

By the end of this chapter, you will be able to:
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]

## Introduction

[Introduction content to be added]

## Core Concepts

### Concept 1

[Content to be added]

### Concept 2

[Content to be added]

## Code Examples

```python
# Example code to be added
```

## Lab Tasks

1. **Task 1**: [Description]
2. **Task 2**: [Description]

## Summary

[Summary to be added]

## References

- [Reference 1]
- [Reference 2]
"""


# Singleton instance
chapter_writer = ChapterWriterAgent()
