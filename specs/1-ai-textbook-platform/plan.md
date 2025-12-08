# Implementation Plan: Physical AI & Humanoid Robotics — AI-Native Textbook

**Branch**: `1-ai-textbook-platform` | **Date**: 2025-12-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/1-ai-textbook-platform/spec.md`
**Version**: 2.0.0

## Summary

Build a production-ready AI-native textbook platform for Physical AI & Humanoid Robotics using Docusaurus for the frontend with modern UI (hero section, animated module cards), FastAPI + Qdrant for the RAG chatbot backend, BetterAuth for authentication, and on-demand personalization/Urdu translation features. The platform follows Modules 1-4 + Capstone structure across Weeks 1-13.

## Technical Context

**Language/Version**: TypeScript 5.x (Frontend), Python 3.11 (Backend)
**Primary Dependencies**: Docusaurus 3.x, React 18, FastAPI, Qdrant Client, BetterAuth, OpenAI SDK
**Storage**: Qdrant Cloud Free Tier (vectors), Neon Postgres (user metadata)
**Testing**: Jest + React Testing Library (Frontend), pytest (Backend)
**Target Platform**: Web (GitHub Pages/Vercel for static, Cloud for API)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: < 2s query latency (local), < 500ms retrieval (cloud), responsive UI
**Constraints**: Qdrant Cloud Free Tier limits, public GitHub repo, deadline 2025-11-30
**Scale/Scope**: ~50 chapters, 4 modules + capstone, single-tenant educational platform

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. AI-Native Development (NON-NEGOTIABLE) | ✅ PASS | Claude Code subagents for chapter generation, quiz creation, personalization skills |
| II. Spec-Driven Development | ✅ PASS | Following Spec-Kit Plus workflow: spec.md → plan.md → tasks.md |
| III. Accessibility & Internationalization | ✅ PASS | Urdu translation button, personalization for different skill levels |
| IV. Production-Ready Architecture | ✅ PASS | Docusaurus + FastAPI + Qdrant + BetterAuth + GitHub Actions CI/CD |
| V. Test-First Approach (NON-NEGOTIABLE) | ✅ PASS | TDD workflow enforced, Jest/pytest for testing |
| VI. Integration & Interoperability | ✅ PASS | Contract testing between frontend/backend, proper error handling |

**Gate Status**: ✅ All principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-textbook-platform/
├── plan.md              # This file
├── spec.md              # Feature specification v2.0.0
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   └── api-contracts.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
frontend/
├── docusaurus.config.js     # Docusaurus configuration
├── src/
│   ├── components/
│   │   ├── Hero/            # Landing page hero section
│   │   ├── ModuleCard/      # Animated module cards
│   │   ├── ChatBot/         # Floating ChatBot widget
│   │   ├── Personalize/     # Personalization button
│   │   ├── TranslateUrdu/   # Urdu translation button
│   │   └── ChapterQuiz/     # Quiz component
│   ├── pages/
│   │   └── index.tsx        # Landing page
│   ├── theme/               # Custom Docusaurus theme
│   └── css/
│       └── custom.css       # Global styles, animations
├── docs/
│   ├── module-1/            # ROS2 Fundamentals (Weeks 1-3)
│   ├── module-2/            # Gazebo/Unity Simulation (Weeks 4-6)
│   ├── module-3/            # Isaac Platform (Weeks 7-9)
│   ├── module-4/            # VLA Models (Weeks 10-12)
│   └── capstone/            # Capstone Project (Week 13)
├── static/
│   ├── img/                 # Icons, logos, favicon
│   └── fonts/               # Custom fonts
└── tests/
    ├── components/          # Component unit tests
    └── integration/         # Integration tests

backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py      # ChatBot endpoints
│   │   │   ├── auth.py      # BetterAuth integration
│   │   │   ├── personalize.py # Personalization endpoints
│   │   │   └── translate.py # Urdu translation endpoints
│   │   └── main.py          # FastAPI app entry
│   ├── services/
│   │   ├── rag.py           # RAG retrieval service
│   │   ├── embeddings.py    # OpenAI embeddings
│   │   ├── personalization.py # Content adaptation
│   │   └── translation.py   # LLM translation
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── chapter.py       # Chapter metadata
│   │   └── chunk.py         # Vector chunk model
│   └── db/
│       ├── qdrant.py        # Qdrant client
│       └── postgres.py      # Neon Postgres client
├── tests/
│   ├── contract/            # API contract tests
│   ├── integration/         # Integration tests
│   └── unit/                # Unit tests
├── requirements.txt         # Python dependencies
└── Dockerfile               # Container configuration

.github/
└── workflows/
    ├── frontend.yml         # Frontend CI/CD
    └── backend.yml          # Backend CI/CD
```

**Structure Decision**: Web application pattern selected based on frontend (Docusaurus) + backend (FastAPI) architecture. Frontend deploys to GitHub Pages/Vercel as static site. Backend deploys to cloud with Docker.

## Complexity Tracking

> No violations identified. Architecture follows constitution principles with justified complexity for the required features.

## Sprint Overview

Based on user input, the project follows 7 sprints:

| Sprint | Name | Goals | Deliverables |
|--------|------|-------|--------------|
| 1 | Repo & Frontend Setup | Git repo, Docusaurus skeleton, landing page hero, theme | Public repo with config, sample chapter, hero |
| 2 | Frontend Module Cards & Animations | Module cards with hover, icons, colors, favicon, responsive | Landing page matching reference UI |
| 3 | Claude Code Subagents & Chapters | Module 1-2 chapters via subagents, quiz/summary/validator skills | MDX files for Weeks 1-7 |
| 4 | RAG Backend + ChatBot UI | FastAPI backend, Qdrant indexing, ChatBot widget | Floating ChatBot functional |
| 5 | BetterAuth & Personalization | Signup/Signin, per-chapter Personalize button | Profile stored, personalized content |
| 6 | Urdu Translation & Chapter Polish | Translate button, chapter layout polish | Chapters with all features |
| 7 | CI/CD & Deployment | GitHub Actions, Docker deployment, demo video | Public book URL, submission ready |
