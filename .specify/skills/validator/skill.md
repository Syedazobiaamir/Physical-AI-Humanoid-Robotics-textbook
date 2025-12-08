# Validator Skill

Perform consistency and style validation on textbook chapter content.

## Purpose

This skill checks chapter content for terminology consistency, style adherence, code correctness, and alignment with the textbook's educational standards.

## Input Requirements

```json
{
  "content": "string",              // Chapter content to validate
  "chapter_id": "string",           // Chapter identifier
  "validation_rules": {
    "terminology": "boolean",       // Check term consistency
    "code_style": "boolean",        // Validate code formatting
    "structure": "boolean",         // Check chapter structure
    "accessibility": "boolean",     // Check accessibility
    "links": "boolean"              // Validate external links
  },
  "reference_chapters": ["string"], // Previous chapters for consistency
  "glossary_path": "string",        // Path to terminology glossary
  "style_guide_path": "string"      // Path to style guide
}
```

## Output Format

```json
{
  "chapter_id": "string",
  "validation_status": "pass|warn|fail",
  "score": {
    "overall": "number (0-100)",
    "terminology": "number",
    "code_quality": "number",
    "structure": "number",
    "accessibility": "number"
  },
  "issues": [
    {
      "id": "string",
      "severity": "error|warning|suggestion",
      "category": "terminology|code|structure|style|accessibility|link",
      "location": {
        "line": "number",
        "section": "string"
      },
      "message": "string",
      "suggestion": "string",
      "auto_fixable": "boolean"
    }
  ],
  "terminology_report": {
    "consistent_terms": ["string"],
    "inconsistent_terms": [
      {
        "term": "string",
        "variants_found": ["string"],
        "preferred": "string"
      }
    ],
    "undefined_terms": ["string"]
  },
  "code_report": {
    "languages_found": ["string"],
    "syntax_valid": "boolean",
    "style_issues": ["string"]
  }
}
```

## Example Usage

### CLI
```bash
claude-code skill validator --input chapter.mdx --rules all --output validation-report.json
```

### API
```python
from specify.skills import Validator

validator = Validator()
report = validator.validate({
    "content": chapter_content,
    "chapter_id": "week-2-nodes-topics",
    "validation_rules": {
        "terminology": True,
        "code_style": True,
        "structure": True,
        "accessibility": True,
        "links": True
    },
    "reference_chapters": ["week-1-intro"],
    "glossary_path": ".specify/glossary.json",
    "style_guide_path": ".specify/style-guide.md"
})

if report["validation_status"] == "fail":
    for issue in report["issues"]:
        if issue["severity"] == "error":
            print(f"ERROR: {issue['message']}")
```

## Validation Rules

### Terminology Consistency

**Preferred Terms:**
| Incorrect | Correct |
|-----------|---------|
| ROS 2, ros2 | ROS2 |
| Gazebo Classic | Gazebo 11 |
| ign gazebo | Ignition Gazebo |
| ubuntu | Ubuntu |
| python | Python |
| c++ | C++ |

**Technical Terms Must:**
- Use consistent capitalization
- Match glossary definitions
- Be introduced before use

### Code Style

**Python:**
- Follow PEP 8 guidelines
- Include type hints for function signatures
- Use meaningful variable names
- Include docstrings for classes/functions

**C++:**
- Follow ROS2 C++ style guide
- Use `auto` appropriately
- Include header guards or `#pragma once`

**Bash:**
- Include comments for complex commands
- Use `#!/bin/bash` shebang
- Quote variables properly

### Structure Requirements

Every chapter MUST include:
- [ ] Frontmatter with sidebar_position, title, description
- [ ] Component imports (ChapterQuiz, ChatSelection)
- [ ] Learning Objectives section (4-6 items)
- [ ] Introduction section
- [ ] At least one Theory section
- [ ] At least one Lab Tasks section
- [ ] Code Examples section
- [ ] Summary section
- [ ] Additional Resources section
- [ ] ChapterQuiz component at end

### Accessibility Checks

- All images have alt text
- Code blocks have language specified
- Headings follow proper hierarchy (no skipping levels)
- Links have descriptive text (not "click here")
- Color is not the only means of conveying information

### Link Validation

- Check all external links are reachable
- Verify internal links point to existing content
- Flag links to deprecated documentation

## Severity Definitions

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| error | Must fix before publishing | Block publish |
| warning | Should fix, impacts quality | Review needed |
| suggestion | Nice to have improvement | Optional |

## Example Output

```json
{
  "chapter_id": "week-2-nodes-topics",
  "validation_status": "warn",
  "score": {
    "overall": 87,
    "terminology": 95,
    "code_quality": 90,
    "structure": 100,
    "accessibility": 75
  },
  "issues": [
    {
      "id": "term-001",
      "severity": "warning",
      "category": "terminology",
      "location": {"line": 45, "section": "Theory"},
      "message": "Inconsistent term: 'ros2' should be 'ROS2'",
      "suggestion": "Replace 'ros2' with 'ROS2'",
      "auto_fixable": true
    },
    {
      "id": "access-001",
      "severity": "warning",
      "category": "accessibility",
      "location": {"line": 78, "section": "Lab Tasks"},
      "message": "Image missing alt text",
      "suggestion": "Add descriptive alt attribute to image",
      "auto_fixable": false
    },
    {
      "id": "code-001",
      "severity": "suggestion",
      "category": "code",
      "location": {"line": 112, "section": "Code Examples"},
      "message": "Consider adding type hints to function parameters",
      "suggestion": "def callback(self, msg: String) -> None:",
      "auto_fixable": true
    }
  ],
  "terminology_report": {
    "consistent_terms": ["ROS2", "Gazebo", "Ubuntu", "Python"],
    "inconsistent_terms": [
      {
        "term": "ROS2",
        "variants_found": ["ros2", "ROS 2"],
        "preferred": "ROS2"
      }
    ],
    "undefined_terms": []
  }
}
```

## Integration

This skill:
- Runs automatically in CI/CD pipeline
- Called by **chapter-writer** for final validation
- Powers the content quality dashboard
- Supports auto-fix for eligible issues
