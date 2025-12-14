---
id: 001
title: Create Unified Design System Spec
stage: spec
date: 2025-12-13
surface: agent
model: claude-opus-4-5-20251101
feature: 001-unified-design-system
branch: 001-unified-design-system
user: Zobia Amir
command: /sp.specify
labels: ["spec", "design-system", "ui-ux", "chatbot", "auth", "personalization"]
links:
  spec: specs/001-unified-design-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-unified-design-system/spec.md
  - specs/001-unified-design-system/checklists/requirements.md
tests:
  - null
---

## Prompt

Unified UI/UX + Chatbot Design System

Design Goal: Create a single, coherent visual language for:

Frontend (Landing + Book)

RAG Chatbot UI

Auth & personalization flows

Global Color Theme:

Deep Space Blue: #0B1020

Neural Indigo: #1E2A78

Electric Cyan: #00E5FF

Soft AI Violet: #7C7CFF

Neutrals: Text Primary #EAEAF0, Muted #9AA4BF, Card Background #121830, Divider #1F2A44

Typography:

Headings: Space Grotesk

Body: Inter

Code: JetBrains Mono

H1: 48px, H2: 36px, H3: 28px, Body: 16–18px

Frontend Landing Page UI (Docusaurus Home)

Hero Section: robotics illustration, subtle motion, gradient glow, CTA buttons

Animated Knowledge Cards (Physical AI topics) with hover lift, cyan glow, icon rotation

Course Roadmap: vertical timeline with animated dots

Navbar: sticky, transparent → solid on scroll, active link glow

Footer: dark, links, subtle grid pattern

Book Content System

Written via Claude Code

MDX with interactive components

Diagrams: robot architecture, AI control loops

RAG Chatbot UI + UX

Colors match frontend theme

AI & user message bubbles, rounded corners, typing animation

"Ask about selected text" button

Context indicator (chapter info)

Floating button, full-screen modal

Uses Gemini API key for AI answers

Authentication & Personalization

Better-Auth integration: Signup / Signin

Collect: Software/Hardware background, skill level, language preference

Neon Serverless Postgres stores user profile & preferences

Personalization button triggers BeginnerSimplifierAgent & HardwareContextAgent

Urdu translation toggle respects user language preference

Subagents & Agent Skills (Bonus)

5 subagents: PhysicalAIInstructor, EmbodiedIntelligenceAgent, BeginnerSimplifierAgent, HardwareContextAgent, UrduTranslationAgent

6 skills: simplify_for_beginner, hardware_mapping, real_world_robot_example, exam_ready_summary, urdu_translate, context_only_answer

Databases: Qdrant Cloud (embeddings), Neon Serverless Postgres (user data)

Deployment: Vercel (frontend), serverless functions (backend)

## Response snapshot

Created comprehensive feature specification for Unified UI/UX + Chatbot Design System:

**Branch**: `001-unified-design-system`

**User Stories (5 prioritized)**:
1. P1: Landing Page Experience - Hero, animated cards, roadmap, navbar, footer
2. P2: RAG Chatbot Interaction - Floating button, text selection, context awareness
3. P3: User Authentication - Better-Auth signup/signin with profile collection
4. P4: Content Personalization - BeginnerSimplifier & HardwareContext agents
5. P5: Urdu Translation - Multilingual support with preference persistence

**Functional Requirements (31)**: Design system core, landing page, book content, chatbot, auth, subagents, deployment

**Key Entities**: User Profile, Chapter, Chat Session, Design Token

**Success Criteria (10)**: Performance metrics, completion rates, consistency scores

**Quality Validation**: All checklist items pass - spec is ready for planning

## Outcome

- ✅ Impact: Complete feature specification created with 5 user stories, 31 functional requirements, 10 success criteria
- 🧪 Tests: N/A (spec phase)
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.clarify (if needed) or /sp.plan to generate implementation plan
- 🧠 Reflection: User provided comprehensive input with explicit design tokens, making spec creation straightforward with no clarifications needed

## Evaluation notes (flywheel)

- Failure modes observed: None - user input was thorough
- Graders run and results (PASS/FAIL): Manual checklist validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
