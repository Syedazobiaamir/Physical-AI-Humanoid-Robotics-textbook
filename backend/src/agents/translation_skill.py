"""
Urdu Translation Skill for Claude Code Subagent

This module provides a skill interface for translating textbook content
from English to Urdu while preserving technical accuracy and formatting.
"""
from typing import Optional, Dict, List
import json


class UrduTranslationSkill:
    """
    Skill for translating educational content to Urdu

    This skill is designed to be used as a Claude Code subagent capability
    for translating Physical AI & Humanoid Robotics textbook content.

    Features:
    - Preserves code blocks and markdown formatting
    - Handles technical term transliteration
    - Maintains document structure (headings, lists, tables)
    - Provides glossary entries for complex terms
    """

    SKILL_NAME = "urdu_translation"
    SKILL_VERSION = "1.0.0"

    # Translation context and guidelines
    TRANSLATION_CONTEXT = """
You are translating educational content about Physical AI and Humanoid Robotics
from English to Urdu. This content is for university-level students in Pakistan.

GUIDELINES:
1. Use formal Urdu (فصیح اردو) suitable for academic texts
2. Keep all technical terms in English with Urdu transliteration in parentheses
3. Preserve ALL markdown formatting:
   - Headings (# ## ###)
   - Code blocks (``` ```)
   - Lists (- or 1.)
   - Bold (**text**) and italic (*text*)
   - Links [text](url)
4. Maintain the same paragraph structure
5. For complex sentences, prioritize clarity over literal translation
6. Add brief explanatory notes for culturally specific examples if needed
"""

    # Technical terms glossary
    TECHNICAL_GLOSSARY: Dict[str, Dict[str, str]] = {
        "robot": {
            "urdu": "روبوٹ",
            "transliteration": "robot",
            "definition": "خودکار مشین جو پروگرام کی ہدایات پر عمل کرتی ہے"
        },
        "sensor": {
            "urdu": "حساس آلہ",
            "transliteration": "sensor",
            "definition": "ماحول سے معلومات حاصل کرنے والا آلہ"
        },
        "actuator": {
            "urdu": "فعال آلہ",
            "transliteration": "actuator",
            "definition": "حرکت پیدا کرنے والا آلہ"
        },
        "algorithm": {
            "urdu": "الگورتھم",
            "transliteration": "algorithm",
            "definition": "مسئلہ حل کرنے کے لیے قدم بہ قدم ہدایات"
        },
        "kinematics": {
            "urdu": "حرکیات",
            "transliteration": "kinematics",
            "definition": "حرکت کا ریاضیاتی مطالعہ"
        },
        "dynamics": {
            "urdu": "حرکیات",
            "transliteration": "dynamics",
            "definition": "قوتوں اور حرکت کا مطالعہ"
        },
        "trajectory": {
            "urdu": "راستہ",
            "transliteration": "trajectory",
            "definition": "حرکت کا منصوبہ بند راستہ"
        },
        "localization": {
            "urdu": "مقام تعین",
            "transliteration": "localization",
            "definition": "روبوٹ کی اپنی پوزیشن معلوم کرنا"
        },
        "mapping": {
            "urdu": "نقشہ سازی",
            "transliteration": "mapping",
            "definition": "ماحول کا نقشہ بنانا"
        },
        "navigation": {
            "urdu": "راہ یابی",
            "transliteration": "navigation",
            "definition": "مقصد تک راستہ تلاش کرنا"
        },
        "perception": {
            "urdu": "ادراک",
            "transliteration": "perception",
            "definition": "ماحول کو سمجھنا"
        },
        "planning": {
            "urdu": "منصوبہ بندی",
            "transliteration": "planning",
            "definition": "عمل کا راستہ طے کرنا"
        },
        "control": {
            "urdu": "کنٹرول",
            "transliteration": "control",
            "definition": "نظام کو منظم کرنا"
        },
        "feedback": {
            "urdu": "فیڈ بیک",
            "transliteration": "feedback",
            "definition": "نتائج کی بنیاد پر تصحیح"
        },
        "neural network": {
            "urdu": "عصبی نیٹ ورک",
            "transliteration": "neural network",
            "definition": "دماغ کی طرح سیکھنے والا نظام"
        },
        "deep learning": {
            "urdu": "ڈیپ لرننگ",
            "transliteration": "deep learning",
            "definition": "گہری سیکھ"
        },
        "reinforcement learning": {
            "urdu": "ریانفورسمنٹ لرننگ",
            "transliteration": "reinforcement learning",
            "definition": "انعام کی بنیاد پر سیکھنا"
        },
    }

    def __init__(self):
        self.context = self.TRANSLATION_CONTEXT
        self.glossary = self.TECHNICAL_GLOSSARY

    def get_skill_info(self) -> Dict:
        """Get skill metadata"""
        return {
            "name": self.SKILL_NAME,
            "version": self.SKILL_VERSION,
            "description": "Translates educational content from English to Urdu",
            "capabilities": [
                "translate_content",
                "preserve_formatting",
                "handle_technical_terms",
                "generate_glossary"
            ]
        }

    def get_translation_prompt(
        self,
        content: str,
        include_glossary: bool = True,
        context_hint: Optional[str] = None
    ) -> str:
        """
        Generate a translation prompt for Claude

        Args:
            content: Content to translate
            include_glossary: Whether to include glossary in prompt
            context_hint: Optional additional context about the content

        Returns:
            Formatted prompt for translation
        """
        prompt_parts = [self.context]

        if context_hint:
            prompt_parts.append(f"\nADDITIONAL CONTEXT: {context_hint}")

        if include_glossary:
            glossary_text = self._format_glossary()
            prompt_parts.append(f"\nTECHNICAL GLOSSARY:\n{glossary_text}")

        prompt_parts.append(f"\nCONTENT TO TRANSLATE:\n{content}")

        prompt_parts.append("""
TRANSLATION OUTPUT:
- Provide the complete Urdu translation
- Maintain all markdown formatting
- For technical terms, use format: English (اردو)
- Ensure code blocks remain unchanged
""")

        return "\n".join(prompt_parts)

    def _format_glossary(self) -> str:
        """Format glossary for prompt inclusion"""
        lines = []
        for term, info in self.glossary.items():
            lines.append(f"- {term}: {info['urdu']} ({info['transliteration']})")
        return "\n".join(lines)

    def get_glossary_entries(self, content: str) -> List[Dict]:
        """
        Extract glossary entries relevant to the content

        Args:
            content: Content to analyze

        Returns:
            List of relevant glossary entries
        """
        relevant_entries = []
        content_lower = content.lower()

        for term, info in self.glossary.items():
            if term.lower() in content_lower:
                relevant_entries.append({
                    "term": term,
                    "urdu": info["urdu"],
                    "transliteration": info["transliteration"],
                    "definition": info["definition"]
                })

        return relevant_entries

    def validate_translation(self, original: str, translated: str) -> Dict:
        """
        Validate translation quality

        Args:
            original: Original English content
            translated: Translated Urdu content

        Returns:
            Validation report
        """
        issues = []

        # Check code block preservation
        original_code_blocks = original.count("```")
        translated_code_blocks = translated.count("```")
        if original_code_blocks != translated_code_blocks:
            issues.append({
                "type": "code_block_mismatch",
                "message": f"Code block count changed: {original_code_blocks} -> {translated_code_blocks}"
            })

        # Check heading preservation
        original_headings = sum(1 for line in original.split('\n') if line.startswith('#'))
        translated_headings = sum(1 for line in translated.split('\n') if line.startswith('#'))
        if original_headings != translated_headings:
            issues.append({
                "type": "heading_mismatch",
                "message": f"Heading count changed: {original_headings} -> {translated_headings}"
            })

        # Check link preservation
        original_links = original.count("](")
        translated_links = translated.count("](")
        if original_links != translated_links:
            issues.append({
                "type": "link_mismatch",
                "message": f"Link count changed: {original_links} -> {translated_links}"
            })

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "stats": {
                "original_length": len(original),
                "translated_length": len(translated),
                "expansion_ratio": len(translated) / len(original) if original else 0
            }
        }

    def to_json(self) -> str:
        """Serialize skill configuration to JSON"""
        return json.dumps({
            "skill": self.get_skill_info(),
            "context": self.context,
            "glossary": self.glossary
        }, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "UrduTranslationSkill":
        """Create skill instance from JSON"""
        data = json.loads(json_str)
        skill = cls()
        skill.context = data.get("context", cls.TRANSLATION_CONTEXT)
        skill.glossary = data.get("glossary", cls.TECHNICAL_GLOSSARY)
        return skill


# Skill usage example for Claude Code integration
SKILL_USAGE_EXAMPLE = """
# Using the Urdu Translation Skill

## Basic Translation
```python
from backend.src.agents.translation_skill import UrduTranslationSkill

skill = UrduTranslationSkill()

# Generate translation prompt
content = "# Introduction to ROS2\\nROS2 is a robotics middleware..."
prompt = skill.get_translation_prompt(content)

# Send to Claude for translation
# translated = claude.complete(prompt)
```

## With Claude Code Subagent
When using as a subagent skill, the skill provides:
1. Translation context and guidelines
2. Technical glossary for consistency
3. Validation of translation quality
4. Formatting preservation checks

The skill is designed to work with the Claude Code subagent framework
for automated content generation.
"""
