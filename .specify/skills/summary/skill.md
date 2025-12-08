# Summary Skill

Extract key points and generate concise summaries from textbook chapter content.

## Purpose

This skill analyzes chapter content and extracts the most important concepts, facts, and takeaways. It produces structured summaries suitable for review sections, flashcards, or quick reference guides.

## Input Requirements

```json
{
  "content": "string",              // Full chapter content (MDX/Markdown)
  "chapter_id": "string",           // Chapter identifier
  "max_points": "number",           // Maximum key points (default: 8)
  "summary_length": "short|medium|long", // Output length
  "include_code_refs": "boolean",   // Reference code examples
  "target_audience": "beginner|intermediate|advanced"
}
```

## Output Format

```json
{
  "chapter_id": "string",
  "title": "string",
  "key_points": [
    {
      "concept": "string",
      "explanation": "string",
      "importance": "high|medium|low",
      "related_code": "string|null"
    }
  ],
  "summary": {
    "short": "string",      // 1-2 sentences
    "medium": "string",     // 1 paragraph
    "long": "string"        // 2-3 paragraphs
  },
  "prerequisites_recap": ["string"],
  "next_steps": ["string"],
  "glossary": [
    {
      "term": "string",
      "definition": "string"
    }
  ]
}
```

## Example Usage

### CLI
```bash
claude-code skill summary --input chapter.mdx --format json --max-points 6
```

### API
```python
from specify.skills import Summary

summarizer = Summary()
result = summarizer.extract({
    "content": chapter_content,
    "chapter_id": "week-1-intro",
    "max_points": 6,
    "summary_length": "medium",
    "include_code_refs": True,
    "target_audience": "beginner"
})

print(result["key_points"])
```

## Extraction Rules

### Key Point Selection
1. Prioritize concepts that appear in learning objectives
2. Include any definitions or new terminology
3. Highlight practical skills demonstrated in lab tasks
4. Note common mistakes or important warnings
5. Capture relationships between concepts

### Summary Generation
- **Short**: Core concept + primary application
- **Medium**: Context + core concepts + key implications
- **Long**: Full narrative covering why, what, how, and next steps

### Glossary Generation
- Extract technical terms introduced in the chapter
- Provide concise, accurate definitions
- Include acronyms with expansions (e.g., "DDS - Data Distribution Service")

## Quality Criteria

- Each key point must be verifiable from the source content
- Summaries must accurately represent chapter scope
- No introduction of concepts not covered in the chapter
- Appropriate complexity for target audience level

## Integration

This skill is called by:
- **chapter-writer** skill for auto-generating Summary sections
- Used standalone for creating study guides
- Powers the "Key Takeaways" feature in the platform

## Example Output

```json
{
  "chapter_id": "week-1-intro",
  "title": "Introduction to ROS2",
  "key_points": [
    {
      "concept": "ROS2 Architecture",
      "explanation": "ROS2 uses DDS as middleware, providing real-time capabilities and multi-platform support",
      "importance": "high",
      "related_code": null
    },
    {
      "concept": "Nodes",
      "explanation": "Fundamental units of computation that communicate via topics, services, and actions",
      "importance": "high",
      "related_code": "HelloWorldPublisher class"
    },
    {
      "concept": "Topics",
      "explanation": "Named publish-subscribe channels for streaming data between nodes",
      "importance": "high",
      "related_code": "self.create_publisher(String, 'hello_topic', 10)"
    }
  ],
  "summary": {
    "short": "ROS2 is a middleware framework for robot software development, built on DDS for real-time and multi-platform support.",
    "medium": "ROS2 represents a major evolution from ROS1, introducing DDS-based communication for real-time capabilities. The framework organizes robot software into nodes that communicate through topics (streaming), services (request-response), and actions (long-running tasks). Setting up ROS2 involves installing the distribution and understanding the workspace structure.",
    "long": "..."
  },
  "glossary": [
    {"term": "DDS", "definition": "Data Distribution Service - industry-standard middleware for real-time systems"},
    {"term": "Node", "definition": "A modular unit of computation in ROS2 that performs a specific function"},
    {"term": "Topic", "definition": "A named bus for publish-subscribe communication between nodes"}
  ]
}
```
