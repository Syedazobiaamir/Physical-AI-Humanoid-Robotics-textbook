---
id: 004
title: Update Constitution v4 Unified Theme
stage: constitution
date: 2025-12-15
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 001-unified-design-system
user: GibTek
command: /sp.constitution
labels: ["constitution", "unified-theme", "dark-blue-yellow", "ai-first", "trust-safety"]
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

Build an AI-Native Technical Textbook Platform that teaches Physical AI & Humanoid Robotics using
interactive content, embedded AI skills, reusable subagents, personalization, and multilingual access.
Non-Negotiable Principles
Single Unified Theme
Dark Blue + Yellow brand system
Same visual identity across Landing Page, Book, Auth, Chatbot, Dashboard
AI-First Design
Every major user interaction uses AI skills
Chatbot provides functionality through reusable skills and subagents, not a fully autonomous agent
Spec-Driven Development
No feature without a spec
UI/UX governed by UIUX Theme Addendum
User Trust & Safety
Secure authentication
Clear AI limitations
Transparent data usage
Performance & Accessibility
Fast load
Keyboard accessible
Mobile responsive

## Response snapshot

Updated constitution from v3.0.0 to v4.0.0 (MAJOR version bump) with the following changes:

1. **Single Unified Theme** (Principle I): Dark Blue (#1a1a2e) + Yellow (#ffd700) brand system with consistent visual identity across all components
2. **AI-First Design** (Principle II): Chatbot MUST use reusable skills and subagents, NOT autonomous agents
3. **Spec-Driven Development** (Principle III): No feature without spec; UI/UX governed by UIUX Theme Addendum
4. **User Trust & Safety** (Principle IV): NEW principle for authentication, AI limitations, and data transparency
5. **Performance & Accessibility** (Principle V): Fast load, keyboard accessible, mobile responsive, WCAG 2.1 AA

Project renamed to "AI-Native Technical Textbook Platform" to reflect broader scope.

## Outcome

- Impact: MAJOR - Principles completely redefined with new focus areas
- Tests: N/A (governance document)
- Files: 1 modified (.specify/memory/constitution.md)
- Next prompts: Create UIUX Theme Addendum document, implement unified theme across components
- Reflection: Clean separation of concerns across 5 principles with clear MUST/MAY language

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review PASS - all placeholders resolved, version correct
- Prompt variant (if applicable): N/A
- Next experiment: Ensure UIUX Theme Addendum is created before any UI implementation
