# Implementation Plan: Unified UI/UX + Chatbot Design System

**Branch**: `001-unified-design-system` | **Date**: 2025-12-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-unified-design-system/spec.md`

## Summary

Create a unified design system for the Physical AI & Humanoid Robotics Course platform, encompassing:
- **Frontend**: Docusaurus-based landing page with hero section, animated knowledge cards, course roadmap, sticky navbar, and dark footer
- **RAG Chatbot**: Floating chat widget with full-screen modal, text selection context, Gemini API integration
- **Authentication**: Better-Auth signup/signin with user profile collection (background, skill level, language preference)
- **Personalization**: AI agents (BeginnerSimplifier, HardwareContext) for content adaptation
- **Translation**: UrduTranslationAgent for multilingual support

Technical approach uses Docusaurus (React) for frontend, FastAPI for backend services, Qdrant for vector search, Neon Postgres for user data, and Vercel for deployment.

## Technical Context

**Language/Version**: TypeScript 5.x (Frontend), Python 3.11 (Backend)
**Primary Dependencies**:
- Frontend: Docusaurus 3.x, React 18, CSS Modules/Tailwind, Framer Motion (animations)
- Backend: FastAPI, Qdrant Client, google-generativeai (Gemini), better-auth, psycopg/asyncpg
**Storage**: Qdrant Cloud (vectors), Neon Serverless Postgres (user profiles)
**Testing**: Vitest/Jest (frontend), pytest (backend)
**Target Platform**: Web (modern browsers), Vercel deployment
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <3s page load, <5s chatbot response, <100ms UI feedback
**Constraints**: Qdrant Cloud free tier, Neon free tier, Vercel serverless limits
**Scale/Scope**: ~100 concurrent users, 4 course modules + appendices

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | ✅ PASS | Feature has formal spec (spec.md) with user stories, requirements, success criteria |
| II. AI-First Authoring | ✅ PASS | RAG chatbot, AI agents (PhysicalAIInstructor, BeginnerSimplifier, etc.), reusable skills |
| III. Modular, Reusable Intelligence | ✅ PASS | 5 subagents + 6 reusable skills defined; components designed for independent operation |
| IV. Production-Grade UI/UX | ✅ PASS | Explicit design tokens, animations, responsive layout, accessibility requirements |
| V. Accessibility & Performance | ✅ PASS | Urdu translation, personalization, performance targets (<3s load, <100ms feedback) |

**Gate Result**: PASS - All constitution principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-unified-design-system/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   ├── chat-api.yaml    # RAG chatbot endpoints
│   ├── auth-api.yaml    # Authentication endpoints
│   └── user-api.yaml    # User profile endpoints
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── design-system/    # Design tokens, base components
│   │   │   ├── tokens.css    # CSS variables for colors, typography
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Modal.tsx
│   │   ├── landing/          # Landing page components
│   │   │   ├── Hero.tsx
│   │   │   ├── KnowledgeCard.tsx
│   │   │   ├── CourseRoadmap.tsx
│   │   │   ├── Navbar.tsx
│   │   │   └── Footer.tsx
│   │   ├── chatbot/          # RAG chatbot UI
│   │   │   ├── ChatWidget.tsx
│   │   │   ├── ChatModal.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── TypingIndicator.tsx
│   │   │   └── TextSelectionButton.tsx
│   │   ├── auth/             # Authentication UI
│   │   │   ├── AuthModal.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   ├── SigninForm.tsx
│   │   │   └── ProfileSetup.tsx
│   │   └── chapter/          # Chapter page components
│   │       ├── PersonalizeButton.tsx
│   │       └── TranslateButton.tsx
│   ├── pages/
│   │   └── index.tsx         # Landing page
│   ├── services/
│   │   ├── chat.ts           # Chat API client
│   │   ├── auth.ts           # Auth API client
│   │   └── user.ts           # User profile API client
│   └── hooks/
│       ├── useTextSelection.ts
│       └── useAuth.ts
└── tests/
    ├── components/
    └── services/

backend/
├── src/
│   ├── models/
│   │   ├── user.py           # User profile model
│   │   ├── chat.py           # Chat session model
│   │   └── chapter.py        # Chapter content model
│   ├── services/
│   │   ├── rag/
│   │   │   ├── embeddings.py # Qdrant embedding service
│   │   │   ├── retrieval.py  # Context retrieval
│   │   │   └── generation.py # Gemini response generation
│   │   ├── agents/
│   │   │   ├── base.py
│   │   │   ├── physical_ai_instructor.py
│   │   │   ├── embodied_intelligence.py
│   │   │   ├── beginner_simplifier.py
│   │   │   ├── hardware_context.py
│   │   │   └── urdu_translation.py
│   │   ├── skills/
│   │   │   ├── simplify_for_beginner.py
│   │   │   ├── hardware_mapping.py
│   │   │   ├── real_world_robot_example.py
│   │   │   ├── exam_ready_summary.py
│   │   │   ├── urdu_translate.py
│   │   │   └── context_only_answer.py
│   │   └── auth/
│   │       └── better_auth.py
│   └── api/
│       ├── chat.py           # /api/chat endpoints
│       ├── auth.py           # /api/auth endpoints
│       ├── user.py           # /api/user endpoints
│       └── personalize.py    # /api/personalize endpoints
└── tests/
    ├── contract/
    ├── integration/
    └── unit/
```

**Structure Decision**: Web application structure with separate frontend (Docusaurus/React) and backend (FastAPI) projects. Frontend deployed to Vercel, backend as serverless functions or alternative cloud service (Render/Railway).

## Complexity Tracking

> No constitution violations requiring justification. Structure follows standard web app patterns.

| Item | Justification |
|------|---------------|
| 5 AI agents | Required by spec (FR-023 to FR-027) for distinct personalization use cases |
| 6 reusable skills | Required by spec (FR-028) for modular intelligence |
| Dual database | Qdrant for vectors (semantic search), Neon for relational data (users) - standard RAG pattern |
