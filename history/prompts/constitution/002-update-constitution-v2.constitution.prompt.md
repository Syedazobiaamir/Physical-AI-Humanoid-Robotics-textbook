---
id: 002
title: Update Constitution to v2.0.0
stage: constitution
date: 2025-12-07
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 1-ai-textbook-platform
user: Zobia Amir
command: /sp.constitution
labels: ["constitution", "governance", "v2.0.0", "metadata"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (governance document)
---

## Prompt

```text
name: "Physical AI & Humanoid Robotics — AI-Native Textbook Project"
version: "2.0.0"
owners:
  - name: "Zobia Amir"
    role: "Lead Author & Designer"
  - name: "Panaversity Hackathon Team"
    role: "Review & Infrastructure"
mission:
  short: "Create an AI-native textbook and platform for Physical AI & Humanoid Robotics using Claude Code + Spec-Kit Plus."
  long: >
    Build a production-ready Docusaurus book with modern frontend UI (like ai-native-book-iota.vercel.app),
    embed a RAG chatbot (Qdrant + FastAPI), implement BetterAuth signup/signin,
    personalization and Urdu translation buttons, and provide CI/CD for GitHub Pages deployment.
scope:include:
    - Docusaurus book content (Modules 1-4 + Capstone + Appendices)
    - Spec-Kit Plus specs for all chapters
    - Claude Code subagents & reusable skills (quiz generator, summaryer, validator)
    - RAG backend: FastAPI, Qdrant, Neon Postgres (user metadata)
    - Frontend: Docusaurus MDX components, ChatKit widget, personalization & Urdu toggle
    - Modern landing page UI: hero, animated module cards, responsive design, icons, animations
    - BetterAuth integration for Signup/Signin
    - Deployment: GitHub Actions to GitHub Pages (or Vercel alternative)
  exclude:
    - Building custom hardware
    - Purchasing robotsconstraints:
  - Submission deadline: "2025-11-30T18:00:00+05:00"
  - Use Qdrant Cloud Free Tier for vectors
  - Use BetterAuth for authentication
  - Must be runnable from public GitHub repo
success_metrics:
  - published_book_url: "public GitHub Pages link"
  - rag_functional: "User can select text in a chapter and ask chatbot; answer uses only selected text when requested"
  - auth_functional: "Signup/Signin via BetterAuth asks software/hardware background questions"
  - personalization: "Per-chapter 'Personalize' button adapts content based on stored profile"
  - urdu_translation: "Per-chapter 'Translate to Urdu' button produces readable Urdu content"
  - frontend_ui: "Landing page, module cards, animations, icons, and ChatBot match reference site"
communication: - channel: "WhatsApp (for live presentation invite)"
  - repo: "GitHub public repository update my sp. constitution file
```

## Response snapshot

Updated the project constitution from v1.1.0 to v2.0.0 with the following changes:

1. **Added Project Metadata Section**: Structured metadata including owners table (Zobia Amir as Lead Author & Designer, Panaversity Hackathon Team for Review & Infrastructure)

2. **Mission Statement**: Added short and long-form mission statements defining the AI-native textbook platform goals

3. **Scope Definition**: Clear in-scope items (Docusaurus book, Spec-Kit Plus specs, RAG backend, frontend components, BetterAuth, deployment) and out-of-scope items (custom hardware, purchasing robots)

4. **Constraints**: Deadline (2025-11-30), Qdrant Cloud Free Tier, BetterAuth requirement, public GitHub repo requirement

5. **Success Metrics Table**: 6 measurable criteria covering published URL, RAG functionality, authentication, personalization, Urdu translation, and frontend UI

6. **Communication Channels**: WhatsApp for presentations, GitHub as public repository

7. **Core Principles**: Retained all 6 principles with "should" replaced by "MUST" for clarity

8. **Templates Validated**: plan-template.md, spec-template.md, and tasks-template.md confirmed consistent with constitution principles

## Outcome

- Impact: MAJOR version bump (1.1.0 → 2.0.0) with comprehensive metadata structure
- Tests: N/A (governance document)
- Files: 1 file modified (.specify/memory/constitution.md)
- Next prompts: Consider running /sp.specify for first feature implementation
- Reflection: Successfully converted user's YAML-style input into well-structured Markdown constitution with proper governance structure

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders resolved, templates validated
- Graders run and results (PASS/FAIL): PASS - no unresolved placeholders, version increment correct, dates in ISO format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - constitution update complete
