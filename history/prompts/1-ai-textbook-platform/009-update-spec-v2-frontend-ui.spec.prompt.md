---
id: 009
title: Update Spec v2.0.0 with Frontend UI
stage: spec
date: 2025-12-07
surface: agent
model: claude-opus-4-5-20251101
feature: 1-ai-textbook-platform
branch: 1-ai-textbook-platform
user: Zobia Amir
command: /sp.specify
labels: ["spec", "frontend-ui", "v2.0.0", "landing-page", "module-cards"]
links:
  spec: specs/1-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-textbook-platform/spec.md
  - specs/1-ai-textbook-platform/checklists/requirements.md
tests:
  - N/A (specification document)
---

## Prompt

```yaml
title: "Spec: Physical AI & Humanoid Robotics — AI-Native Textbook"
version: "2.0.0"
overview: |
  This specification defines the acceptance criteria for the full textbook,
  frontend UI, RAG chatbot, BetterAuth integration, personalization, Urdu translation,
  and deployment pipeline. The book follows Modules 1-4 + Capstone, Weeks 1-13.
components:
  - id: frontend
    name: "Frontend UI"
    description: "Landing page, module cards, chapter pages with ChatBot, personalization, Urdu translation"
    acceptance_criteria:
      - "Landing page hero matches reference site"
      - "Module cards display title, week, icon, animated hover effect"
      - "Chapter pages include: <Personalize />, <TranslateUrdu />, ChatBot widget floating bottom-right"
      - "ChatBot supports selection mode and context mode"
      - "Responsive design and mobile-friendly"
      - "Colors, fonts, favicon, logo, and icons consistent across site"
  - id: book
    name: Docusaurus Book
    description: "Docusaurus site with MDX chapters and interactive components"
    acceptance_criteria:
      - "All modules (ROS2, Gazebo/Unity, Isaac, VLA) have chapters matching weekly breakdown"
      - "Each chapter contains: learning objectives, theory, lab tasks, code examples, quizzes, resources"
      - "MDX components: <Personalize />, <TranslateUrdu />, <ChatSelection />"
      - "GitHub Pages or Vercel deployment URL is valid and public"
  - id: rag
    name: RAG Chatbot
    description: "Retrieval-augmented chatbot using Qdrant, FastAPI, ChatKit/OpenAI Agents"
    acceptance_criteria:
      - "Selected-text mode returns answer constrained to selected text"
      - "Context mode returns top-5 retrieved chunks"
      - "Latency: typical query < 2s for small book (local dev); < 500ms retrieval in cloud"
  - id: auth
    name: BetterAuth Integration
    description: "Signup and Signin flows with background capture"
    acceptance_criteria:
      - "Signup collects: name, email, role, software background, hardware background"
      - "JWT issued and used for personalization endpoints"
  - id: personalization
    name: Personalization Engine
    description: "Generates learning path and content adaptations per user profile"
    acceptance_criteria:
      - "Personalize button at chapter start modifies content: variants 'beginner', 'intermediate', 'advanced'"
      - "Progress tracking recorded in Neon Postgres"
  - id: urdu
    name: Urdu Translation
    description: "On-demand Urdu translation using LLM, preserving formatting"
    acceptance_criteria:
      - "Translate button returns Urdu markdown preserving code blocks and headings"
```

## Response snapshot

Updated the feature specification from v1.1.0 to v2.0.0 with the following key changes:

1. **Added Frontend UI Component**: New component with 7 functional requirements covering:
   - Landing page hero section matching reference site
   - Module cards with title, week, icon, and animated hover effects
   - Floating ChatBot widget at bottom-right
   - Responsive and mobile-friendly design
   - Consistent UI styling (colors, fonts, favicon, logo, icons)

2. **New User Story (P1)**: "Access Modern Landing Page" added as priority P1 to cover the frontend UI experience

3. **Updated Requirements Structure**: Organized 23 functional requirements by component (Frontend UI, Docusaurus Book, RAG Chatbot, BetterAuth, Personalization, Urdu Translation)

4. **Updated Success Criteria**: Added 12 measurable outcomes including new criteria for landing page, module cards, and UI consistency

5. **Added Assumptions Section**: Documented key assumptions including reference site as design target, browser compatibility, and LLM availability

6. **Updated Quality Checklist**: Added v2.0.0 validation section confirming all new frontend requirements are properly specified

## Outcome

- Impact: MAJOR spec update adding Frontend UI component and landing page requirements
- Tests: N/A (specification document)
- Files: 2 files modified (spec.md, requirements.md checklist)
- Next prompts: Run /sp.plan to update implementation plan for v2.0.0 requirements
- Reflection: Successfully incorporated user's YAML component structure into proper spec format with user stories, requirements, and success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None - all requirements testable and unambiguous
- Graders run and results (PASS/FAIL): PASS - all checklist items validated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - spec update complete, ready for planning
