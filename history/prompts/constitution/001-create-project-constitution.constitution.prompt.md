---
id: 1
title: Create Project Constitution
stage: constitution
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: GibTek
command: /sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
 name: "Physical AI & Humanoid Robotics — AI-Native Textbook Project"
version: "1.1.0"
owners:
  - name: "Zobia Amir"
    role: "Lead Author & Designer"
  - name: "Panaversity Hackathon Team"
    role: "Review & Infrastructure"
mission:
  short: "Create an AI-native textbook and platform for Physical AI & Humanoid Robotics using Claude Code + Spec-Kit Plus."
  long: >
    Build a production-ready Docusaurus book, embed a RAG chatbot (Qdrant + FastAPI),
    implement BetterAuth signup/signin, personalization and Urdu translation buttons,
    generate interactive quizzes per chapter, and provide CI/CD for GitHub Pages deployment.
    Use Spec-Kit Plus to drive automated chapter generation, quizzes, and reusable agent skills.scope:
  include:
    - Docusaurus book content (Modules 1-4 + Capstone + Appendices)
    - Spec-Kit Plus specs for all chapters
    - Claude Code subagents & reusable skills (quiz generator, summaryer, validator)
    - RAG backend: FastAPI, Qdrant, Neon Postgres (user metadata)
    - Frontend: Docusaurus MDX components, ChatKit widget, Personalize & Urdu toggle
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
  - quizzes: "All chapters include 5 multiple-choice questions; component renders in Docusaurus"
communication:- channel: "WhatsApp (for live presentation invite)"
  - repo: "GitHub public repository"
```

## Response snapshot

Created the project constitution file (.specify/memory/constitution.md) for the Physical AI & Humanoid Robotics textbook project, incorporating the following principles:
- I. AI-Native Development (NON-NEGOTIABLE)
- II. Spec-Driven Development
- III. Accessibility & Internationalization
- IV. Production-Ready Architecture
- V. Test-First Approach (NON-NEGOTIABLE)
- VI. Integration & Interoperability

The constitution includes additional constraints, development workflow, and governance sections aligned with the project requirements. It specifies technology stack requirements, submission deadline, and compliance expectations.

## Outcome

- ✅ Impact: Project constitution established with 6 core principles and governance structure
- 🧪 Tests: No tests required for this configuration file
- 📁 Files: Updated .specify/memory/constitution.md with project-specific governance
- 🔁 Next prompts: Plan feature development using /sp.plan
- 🧠 Reflection: Constitution provides clear governance framework for AI-native textbook project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A