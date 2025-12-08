---
id: 2
title: Create Textbook Platform Spec
stage: spec
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-ai-textbook-platform
branch: 1-ai-textbook-platform
user: GibTek
command: /sp.specify
labels: [specification, textbook, ai-platform, rag, auth]
links:
  spec: specs/1-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-ai-textbook-platform/spec.md
 - specs/1-ai-textbook-platform/checklists/requirements.md
tests:
 - none
---

## Prompt

```text
title: "Spec: Physical AI & Humanoid Robotics — AI-Native Textbook"
version: "1.1.0"
overview: |
  This specification defines the acceptance criteria for the full textbook,
  the RAG chatbot, BetterAuth integration, personalization, Urdu translation,
  quiz generation, and deployment pipeline. The book follows Modules 1-4 + Capstone, Weeks 1-13.
components:
  - id: book
    name: Docusaurus Book
    description: "Docusaurus site with MDX chapters, interactive components, and quizzes."acceptance_criteria:
      - "All modules (ROS2, Gazebo/Unity, Isaac, VLA) have chapters matching weekly breakdown"
      - "Each chapter contains: learning objectives, theory, lab tasks, code examples, quizzes, resources"
      - "Chapters implement MDX components: <Personalize />, <TranslateUrdu />, <ChatSelection />, <ChapterQuiz />"
      - "GitHub Pages or Vercel deployment URL is valid and public"
  - id: rag
    name: RAG Chatbot
    description: "Retrieval-augmented chatbot using Qdrant, FastAPI, ChatKit/OpenAI Agents"acceptance_criteria:
      - "Selected-text mode: when user selects text and asks 'Answer from selection', the response must be limited to retrieved selection and sources cited"
      - "Context mode: general Q&A returns answers using top-5 retrieved chunks"
      - "Latency: typical query < 2s for small book (local dev); < 500ms retrieval in cloud"
      - "Vector collection updates incrementally on chapter changes"id: auth
    name: BetterAuth Integration
    description: "Signup and Signin flows with background capture"acceptance_criteria:
      - "Signup collects: name, email, role, software background, hardware background (predefined options)"
      - "JWT issued and used for personalization endpoints"
      - "Role-based access enforced in backend (author/student/admin)" id: personalization
    name: Personalization Engine
    description: "Generates learning path and content adaptations per user profile"acceptance_criteria:
      - "Personalize button at chapter start modifies content: example variants 'beginner', 'intermediate', 'advanced'"
      - "Personalization uses stored profile and a small policy (rules + LLM prompt)"
      - "Progress tracking recorded in Neon Postgres" id: urdu
    name: Urdu Translation
    description: "On-demand Urdu translation using LLM (server-side), including inline formatting"acceptance_criteria:
      - "Translate button returns Urdu markdown preserving code blocks and headings"
      - "Translation quality: human-readable; common technical terms either transliterated or provided with glossary"
  - id: quiz
    name: Quiz Generator
    description: "Generates 5 multiple-choice questions per chapter and integrates with MDX component"
    acceptance_criteria:
      - "Each chapter MDX has a corresponding JSON with 5 MCQs + answers"
      - "Frontend <ChapterQuiz /> component renders questions correctly"functionality:
  chapter_generation:
    description: "Subagent 'chapter-writer' generates MDX chapters from spec, including quizzes."
    steps:
      - "Read module and week info from spec"
      - "Generate frontmatter: title, week, learningObjectives"
      - "Generate theory content, lab tasks, code examples"
      - "Generate 5 multiple-choice questions using 'quiz-generator'"
      - "Produce MDX file in docs/module-{n}/"quiz_generator:
    description: "Subagent 'quiz-generator' creates MCQs from chapter text."
    inputs: [chapter_text]
    outputs: [array of 5 questions with 4 options + answer key]
  rag_integration:
    description: "Subagent adds vectorization metadata for Qdrant"
    steps:
      - "Chunk text into 400-600 tokens"
      - "Add metadata: doc_id, chapter, heading, chunk_index"
      - "Push embeddings to Qdrant collection" personalization:
    description: "Generates beginner/intermediate/advanced variants per user profile"
    steps:
      - "Frontend sends JWT + chapter_id + level"
      - "Backend calls 'personalize-skill' subagent"
      - "Return variant content"
  urdu_translation:
    description: "Translate chapter MDX to Urdu while preserving markdown"
    steps:
      - "Send raw markdown to LLM translation skill"
      - "Return preserved code blocks, headings, and lists"
```

## Response snapshot

Created comprehensive specification for the Physical AI & Humanoid Robotics — AI-Native Textbook platform. The spec includes 5 user stories covering core textbook access, RAG chatbot functionality, account creation with personalization, Urdu translation, and quiz completion. All functional requirements are defined with specific capabilities, and success criteria include measurable outcomes for content coverage, response times, and feature functionality. The specification is ready for planning phase.

## Outcome

- ✅ Impact: Complete textbook platform specification with 5 user stories and 16 functional requirements
- 🧪 Tests: No tests required for specification creation
- 📁 Files: Created spec.md and requirements.md checklist in specs/1-ai-textbook-platform/
- 🔁 Next prompts: Plan implementation using /sp.plan
- 🧠 Reflection: Specification covers all major components (book, RAG, auth, personalization, translation, quizzes)

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A