# Quiz Generator Skill

Generate multiple-choice questions (MCQs) with answers for chapter assessment.

## Purpose

This skill creates quiz questions based on chapter content to assess reader comprehension. Questions cover key concepts, code understanding, and practical application.

## Input Requirements

```json
{
  "content": "string",              // Chapter content (MDX/Markdown)
  "chapter_id": "string",           // Chapter identifier
  "num_questions": "number",        // Number of questions (default: 5)
  "difficulty_mix": {               // Distribution of difficulty
    "easy": 0.2,
    "medium": 0.5,
    "hard": 0.3
  },
  "question_types": [               // Types to include
    "concept",                      // Theoretical understanding
    "code",                         // Code comprehension
    "application",                  // Practical scenarios
    "troubleshooting"               // Debug/fix scenarios
  ],
  "include_explanations": "boolean" // Add answer explanations
}
```

## Output Format

```json
{
  "chapter_id": "string",
  "quiz_version": "string",
  "questions": [
    {
      "id": "string",
      "type": "concept|code|application|troubleshooting",
      "difficulty": "easy|medium|hard",
      "question": "string",
      "code_snippet": "string|null",
      "options": [
        {"id": "A", "text": "string"},
        {"id": "B", "text": "string"},
        {"id": "C", "text": "string"},
        {"id": "D", "text": "string"}
      ],
      "correct_answer": "A|B|C|D",
      "explanation": "string",
      "related_section": "string"
    }
  ],
  "metadata": {
    "generated_at": "ISO timestamp",
    "source_chapter": "string",
    "total_questions": "number"
  }
}
```

## Example Usage

### CLI
```bash
claude-code skill quiz-generator --input chapter.mdx --num-questions 5 --output quiz.json
```

### API
```python
from specify.skills import QuizGenerator

generator = QuizGenerator()
quiz = generator.generate({
    "content": chapter_content,
    "chapter_id": "week-1-intro",
    "num_questions": 5,
    "difficulty_mix": {"easy": 0.2, "medium": 0.6, "hard": 0.2},
    "question_types": ["concept", "code", "application"],
    "include_explanations": True
})

for q in quiz["questions"]:
    print(f"Q: {q['question']}")
    print(f"A: {q['correct_answer']} - {q['explanation']}")
```

## Question Generation Guidelines

### Concept Questions (Theoretical)
- Test understanding of definitions and relationships
- Avoid trivial recall; focus on comprehension
- Include "why" questions, not just "what"

Example:
```
What is the primary advantage of ROS2's use of DDS over ROS1's custom middleware?
A) Lower memory usage
B) Built-in real-time and multi-platform support [CORRECT]
C) Simpler API
D) Faster compilation times
```

### Code Questions (Comprehension)
- Show code snippets and ask about behavior
- Test ability to read and understand code
- Include output prediction questions

Example:
```python
# Given this code:
self.publisher_ = self.create_publisher(String, 'hello_topic', 10)
```
```
What does the number '10' represent in this publisher creation?
A) Message size in bytes
B) Queue depth for messages [CORRECT]
C) Publish frequency in Hz
D) Topic priority level
```

### Application Questions (Practical)
- Present real-world scenarios
- Ask for best approach or tool selection
- Test decision-making ability

### Troubleshooting Questions
- Show error messages or broken code
- Ask to identify the problem
- Test debugging skills

## Quality Criteria

### Questions Must:
- Be clearly answerable from chapter content
- Have exactly one correct answer
- Include plausible distractors (wrong answers)
- Avoid "all of the above" or "none of the above"
- Not use negatives ("Which is NOT...")

### Distractors Must:
- Be plausible but clearly wrong
- Address common misconceptions
- Be similar in length to correct answer
- Not be obviously absurd

## Integration

This skill:
- Powers the `<ChapterQuiz />` component
- Is called by **chapter-writer** skill
- Feeds into progress tracking system

## Example Output

```json
{
  "chapter_id": "week-1-intro",
  "quiz_version": "1.0",
  "questions": [
    {
      "id": "q1-ros2-architecture",
      "type": "concept",
      "difficulty": "easy",
      "question": "What middleware does ROS2 use for communication between nodes?",
      "code_snippet": null,
      "options": [
        {"id": "A", "text": "MQTT"},
        {"id": "B", "text": "DDS (Data Distribution Service)"},
        {"id": "C", "text": "REST APIs"},
        {"id": "D", "text": "WebSockets"}
      ],
      "correct_answer": "B",
      "explanation": "ROS2 is built on top of DDS, an industry-standard middleware for real-time distributed systems. This provides features like QoS policies, discovery, and security.",
      "related_section": "Theory: ROS2 Architecture"
    },
    {
      "id": "q2-publisher-code",
      "type": "code",
      "difficulty": "medium",
      "question": "In the following code, what does `timer_period = 1.0` control?",
      "code_snippet": "self.timer = self.create_timer(timer_period, self.timer_callback)",
      "options": [
        {"id": "A", "text": "How long the node runs before shutting down"},
        {"id": "B", "text": "The interval between callback function executions"},
        {"id": "C", "text": "The timeout for receiving messages"},
        {"id": "D", "text": "The message queue timeout"}
      ],
      "correct_answer": "B",
      "explanation": "The timer_period parameter sets how frequently (in seconds) the timer_callback function is called. With 1.0, the callback runs every second.",
      "related_section": "Task 2: Create Your First Node"
    }
  ]
}
```
