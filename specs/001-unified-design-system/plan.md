# Implementation Plan: AI-Native Technical Textbook Platform

**Branch**: `001-unified-design-system` | **Date**: 2025-12-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-unified-design-system/spec.md`

## Summary

Build an AI-Native Technical Textbook Platform with unified Dark Blue (#1a1a2e) + Yellow (#ffd700) theme across all components. The platform features a Docusaurus-based textbook with AI skill buttons (Personalize, Translate, Ask AI), a Next.js landing page with authentication via Clerk, and a FastAPI backend powering RAG chatbot skills using Gemini API with Qdrant embeddings and Neon Postgres storage.

## Technical Context

**Language/Version**: TypeScript 5.x (Frontend), Python 3.11+ (Backend)
**Primary Dependencies**:
- Frontend: Docusaurus 3.x, Next.js 14+, React 18+, Clerk React SDK, Framer Motion
- Backend: FastAPI 0.115+, SQLAlchemy 2.x, Qdrant Client, Google GenAI (Gemini)
**Storage**: Neon Postgres (user profiles, sessions, metadata), Qdrant Cloud (embeddings)
**Testing**: Jest/Vitest (Frontend), pytest (Backend)
**Target Platform**: Vercel (Frontend), Vercel Functions / Railway (Backend)
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**:
- Landing page < 3s load time
- Chatbot response < 5s first token
- 100 concurrent sessions
**Constraints**:
- Dark Blue + Yellow theme consistency (Constitution Principle I)
- Skills-based AI only, no autonomous agents (Constitution Principle II)
- Clerk authentication required (Constitution Principle IV)
**Scale/Scope**: Educational platform, ~50 chapters, ~10k target users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Evidence |
|-----------|-------------|--------|----------|
| I. Single Unified Theme | Dark Blue + Yellow across all components | ✅ PASS | FR-001, FR-010, FR-013, FR-015, FR-032, FR-033 |
| II. AI-First Design | Skills/subagents, not autonomous agents | ✅ PASS | FR-021 to FR-025 define modular skills |
| III. Spec-Driven Development | Spec before implementation | ✅ PASS | spec.md complete with 33 FRs |
| IV. User Trust & Safety | Clerk auth, clear AI limits | ✅ PASS | FR-007 to FR-009 for auth |
| V. Performance & Accessibility | <3s load, keyboard accessible | ✅ PASS | SC-001, SC-008 define metrics |

**Gate Result**: ✅ ALL PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-unified-design-system/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
│   ├── auth-api.yaml
│   ├── rag-api.yaml
│   ├── skills-api.yaml
│   └── stats-api.yaml
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── auth.py           # Clerk webhook handlers
│   │   ├── rag.py            # RAG chatbot endpoints
│   │   ├── personalization.py # Personalization skill
│   │   ├── translation.py    # Urdu translation skill
│   │   └── stats.py          # Platform statistics
│   ├── database/
│   │   ├── base.py           # SQLAlchemy setup
│   │   └── models.py         # Database models
│   ├── llm/
│   │   └── provider.py       # Gemini API client
│   ├── services/
│   │   ├── embedding.py      # Qdrant vector operations
│   │   └── skills/           # Reusable AI skills
│   │       ├── book_retrieval.py
│   │       ├── context_selection.py
│   │       ├── personalization.py
│   │       └── translation.py
│   └── main.py               # FastAPI app
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/
│   │   ├── theme/            # Design system components
│   │   │   ├── ThemeProvider.tsx
│   │   │   ├── colors.ts
│   │   │   └── tokens.ts
│   │   ├── landing/          # Landing page components
│   │   │   ├── Hero.tsx
│   │   │   ├── StatsCards.tsx
│   │   │   ├── FeatureCards.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   └── Footer.tsx
│   │   ├── chatbot/          # RAG chatbot widget
│   │   │   ├── ChatWidget.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   └── ContextSelector.tsx
│   │   └── skills/           # AI skill buttons
│   │       ├── PersonalizeButton.tsx
│   │       ├── TranslateButton.tsx
│   │       └── AskAIButton.tsx
│   ├── theme/
│   │   └── DocItem/          # Docusaurus theme overrides
│   │       └── Layout/
│   │           └── index.tsx
│   └── pages/
│       └── index.tsx         # Landing page (if Next.js)
├── docs/                     # Docusaurus MDX content
│   ├── module-1/
│   ├── module-2/
│   ├── module-3/
│   └── module-4/
└── tests/

shared/
└── theme-tokens.json         # Shared design tokens
```

**Structure Decision**: Web application with separate frontend (Docusaurus + Next.js components) and backend (FastAPI). The frontend serves both the Docusaurus textbook and landing page with shared theme tokens. Backend provides API endpoints for RAG, skills, and user management.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Vercel)                           │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   Landing Page   │  │    Docusaurus    │  │   Auth (Clerk)   │  │
│  │    (Next.js)     │  │    Textbook      │  │                  │  │
│  │                  │  │                  │  │  - Signup        │  │
│  │  - Hero          │  │  - Chapters      │  │  - Login         │  │
│  │  - Stats Cards   │  │  - AI Skills     │  │  - Background    │  │
│  │  - Features      │  │  - ChatWidget    │  │    Questions     │  │
│  │  - Testimonials  │  │                  │  │                  │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Shared Theme System                         │   │
│  │        Dark Blue (#1a1a2e) + Yellow (#ffd700)               │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ API Calls
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI on Vercel/Railway)              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   RAG Chatbot    │  │  AI Skills API   │  │   Auth Webhooks  │  │
│  │                  │  │                  │  │                  │  │
│  │  POST /chat      │  │  POST /personal  │  │  POST /webhook   │  │
│  │  POST /context   │  │  POST /translate │  │                  │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────────────┘  │
│           │                     │                                   │
│           ▼                     ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Skills Layer                              │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │   │
│  │  │Book Content │ │Personalize  │ │Translation  │            │   │
│  │  │   Skill     │ │   Skill     │ │   Skill     │            │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘            │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Neon Postgres  │    │  Qdrant Cloud   │    │   Gemini API    │
│                 │    │                 │    │                 │
│  - Users        │    │  - Embeddings   │    │  - Chat         │
│  - Profiles     │    │  - Vector Search│    │  - Translation  │
│  - Sessions     │    │                 │    │  - Personalize  │
│  - Stats        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## AI Skills Architecture

Per Constitution Principle II, all AI features are implemented as **modular skills**, not autonomous agents:

| Skill | Input | Output | Used By |
|-------|-------|--------|---------|
| Book Content Skill | question, user_profile | RAG response with sources | Chatbot (whole-book) |
| Context Selection Skill | question, selected_text | Response from selected context only | Chatbot (selection) |
| Personalization Skill | chapter_content, user_profile | Adapted content | Personalize button |
| Translation Skill | content, target_lang | Translated content | Translate button |

**Error Handling**: Each skill returns structured responses with `success`, `data`, and `error` fields. UI displays graceful degradation messages when skills fail.

## Complexity Tracking

> No Constitution violations requiring justification.

| Decision | Rationale | Alternative Rejected |
|----------|-----------|---------------------|
| Docusaurus + Next.js | Docusaurus for docs, Next.js for landing | Single framework lacks MDX doc support |
| Clerk over custom auth | Constitution mandates Clerk; faster implementation | Custom auth adds security risk |
| Skills over autonomous agents | Constitution Principle II mandate | Autonomous agents harder to debug/maintain |
