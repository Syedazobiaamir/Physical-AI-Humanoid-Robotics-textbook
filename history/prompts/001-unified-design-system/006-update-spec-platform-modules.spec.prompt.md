---
id: 006
title: Update Spec Platform Modules
stage: spec
date: 2025-12-15
surface: agent
model: claude-opus-4-5-20251101
feature: 001-unified-design-system
branch: 001-unified-design-system
user: GibTek
command: /sp.specify
labels: ["spec", "platform-modules", "landing-page", "auth", "chatbot", "personalization"]
links:
  spec: specs/001-unified-design-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-unified-design-system/spec.md
  - specs/001-unified-design-system/checklists/requirements.md
tests:
  - N/A (specification document)
---

## Prompt

SP.SPECIFY (Functional Requirements)
Platform Modules
1. Landing Page
Hero section with animated gradient background
Signup / Login buttons (top right)
Statistics cards:
Number of books
Active users
AI interactions
Animated feature cards
Testimonials / credibility section
Footer with links, theme-consistent
2. Authentication (Better-Auth)
Signup
Ask user background:
Software level
Hardware exposure
Robotics experience
Login
Session persistence
3. AI-Native Textbook (Docusaurus)
Structured chapters by module
Each chapter includes:
 Personalize Content skill button
 Translate to Urdu skill button
 Ask AI skill button (RAG Chatbot using Gemini API)
4. RAG Chatbot (Gemini API Skills)
Floating chat widget
Theme-matched UI
Supports:
Whole-book questions (Book Content Skill)
Selected-text-only questions (Context Selection Skill)
Tech stack:
FastAPI backend
Gemini API (Anthropic)
Neon Postgres (user profiles)
Qdrant Cloud Free Tier (embeddings)
Features implemented as skills and reusable subagents:
Personalization Skill → modifies response based on user profile
Translation Skill → converts response to Urdu
Book Retrieval Skill → fetches context from textbook
Additional Claude Code Subagents → reusable across multiple chapters or functions
5. Personalization Engine
Adjusts:
Depth of explanation
Code complexity
Hardware assumptions
Uses Personalization Skill to adapt content
Subagents allow reusable intelligence for multiple modules

## Response snapshot

Updated feature specification for AI-Native Technical Textbook Platform with:

**6 User Stories** covering all platform modules:
1. Landing Page Experience (P1) - Hero, statistics, feature cards, testimonials, footer
2. Authentication with Background Collection (P2) - Clerk auth with user background questions
3. AI-Native Textbook Navigation (P3) - Docusaurus with 3 AI skill buttons per chapter
4. RAG Chatbot with AI Skills (P4) - Floating widget with Book Content and Context Selection skills
5. Personalization Engine (P5) - Adjusts content based on user profile
6. Urdu Translation (P6) - Translation skill for multilingual access

**33 Functional Requirements** organized by:
- Landing Page (FR-001 to FR-006)
- Authentication (FR-007 to FR-010)
- AI-Native Textbook (FR-011 to FR-013)
- RAG Chatbot (FR-014 to FR-020)
- AI Skills & Subagents (FR-021 to FR-025)
- Personalization Engine (FR-026 to FR-028)
- Backend Infrastructure (FR-029 to FR-031)
- Theme Compliance (FR-032 to FR-033)

**Key Corrections**:
- Changed "Better-Auth" to Clerk per Constitution v4.0.0
- Corrected "Gemini API (Anthropic)" to "Gemini API (Google)" - Anthropic makes Claude, not Gemini
- Aligned Dark Blue (#1a1a2e) + Yellow (#ffd700) theme throughout

## Outcome

- Impact: Updated spec to reflect comprehensive platform module requirements
- Tests: N/A (specification document)
- Files: 2 modified (spec.md, checklists/requirements.md)
- Next prompts: Run `/sp.plan` to update implementation plan with new requirements
- Reflection: User input was comprehensive; main clarifications were auth provider (Constitution overrides) and API provider naming

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Quality checklist PASS - all items satisfied
- Prompt variant (if applicable): N/A
- Next experiment: Ensure plan.md and tasks.md are updated to reflect new spec requirements
