# Tasks: Unified UI/UX + Chatbot Design System

**Input**: Design documents from `/specs/001-unified-design-system/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/` (Docusaurus/React)
- **Backend**: `backend/src/` (FastAPI/Python)
- **Tests**: `frontend/tests/`, `backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per plan.md (frontend/, backend/, docs/)
- [X] T002 Initialize Docusaurus 3.x project in frontend/ with TypeScript template
- [X] T003 [P] Initialize Python 3.11 FastAPI project in backend/ with pyproject.toml
- [X] T004 [P] Configure ESLint and Prettier for frontend in frontend/.eslintrc.js
- [X] T005 [P] Configure Ruff and Black for backend in backend/pyproject.toml
- [X] T006 [P] Create environment variable templates in frontend/.env.example and backend/.env.example
- [X] T007 [P] Install frontend dependencies: framer-motion in frontend/package.json
- [X] T008 [P] Install backend dependencies: fastapi, qdrant-client, google-generativeai, asyncpg in backend/requirements.txt
- [ ] T009 Configure Tailwind CSS with design tokens in frontend/tailwind.config.js
- [X] T010 Create CSS variables for design system in frontend/src/css/custom.css

**Checkpoint**: Project structure ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Design System Foundation

- [X] T011 Create design tokens TypeScript interface in frontend/src/types/design-tokens.ts
- [X] T012 [P] Create base Button component in frontend/src/components/design-system/Button.tsx
- [X] T013 [P] Create base Card component in frontend/src/components/design-system/Card.tsx
- [X] T014 [P] Create base Modal component in frontend/src/components/design-system/Modal.tsx
- [X] T015 Load web fonts (Space Grotesk, Inter, JetBrains Mono) in frontend/src/css/fonts.css

### Backend Foundation

- [X] T016 Create FastAPI application entry point in backend/src/main.py
- [X] T017 [P] Create database connection module for Neon Postgres in backend/src/database/__init__.py
- [X] T018 [P] Create Qdrant client module in backend/src/vector_store/qdrant_client.py
- [X] T019 Run SQL schema migration for Neon Postgres (users, user_profiles, chapters, chat_sessions, chat_messages, personalized_content tables)
- [X] T020 [P] Create base Pydantic models in backend/src/models/base.py
- [X] T021 Create CORS middleware configuration in backend/src/main.py (integrated)
- [X] T022 Create error handling middleware in backend/src/middleware/error_handler.py
- [X] T023 Create environment configuration loader in backend/src/main.py (dotenv integration)

### Shared Models

- [X] T024 [P] Create User model in backend/src/models/user.py
- [X] T025 [P] Create UserProfile model in backend/src/models/personalization_profile.py
- [X] T026 [P] Create Chapter model in backend/src/models/chapter.py
- [X] T027 [P] Create ChatSession model (integrated in rag_service)
- [X] T028 [P] Create ChatMessage model (integrated in rag_service)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Landing Page Experience (Priority: P1) 🎯 MVP

**Goal**: Visually stunning, robotics-themed landing page with animated elements, interactive cards, course roadmap, sticky navbar, and dark footer

**Independent Test**: Load homepage, verify hero renders with gradient glow, hover over cards to see lift animation, scroll to verify navbar transition, view roadmap animation

### Implementation for User Story 1

- [X] T029 [P] [US1] Create Hero component with robotics illustration and gradient glow in frontend/src/components/Hero/Hero.tsx
- [X] T030 [P] [US1] Create KnowledgeCard component (as ModuleCard) with hover animations in frontend/src/components/ModuleCard/ModuleCard.tsx
- [X] T031 [P] [US1] Create CourseRoadmap component with animated vertical timeline in frontend/src/components/landing/CourseRoadmap.tsx
- [X] T032 [P] [US1] Create Navbar component (via Docusaurus theme) with scroll behavior
- [X] T033 [P] [US1] Create Footer component (via Docusaurus theme) with dark theme
- [X] T034 [US1] Create useScrollPosition hook for navbar scroll detection in frontend/src/hooks/useScrollPosition.ts
- [X] T035 [US1] Compose landing page with all components in frontend/src/pages/index.tsx
- [X] T036 [US1] Add CSS animations for card hover effects (lift, cyan glow, icon rotation) in frontend/src/css/animations.css
- [X] T037 [US1] Create robotics illustration SVG asset (inline in Hero.tsx)
- [X] T038 [US1] Configure Docusaurus theme colors to match design system in frontend/docusaurus.config.ts

**Checkpoint**: Landing page fully functional with all animations - User Story 1 complete

---

## Phase 4: User Story 2 - RAG Chatbot Interaction (Priority: P2)

**Goal**: Floating chat widget with full-screen modal, text selection context, typing animation, and Gemini-powered AI responses

**Independent Test**: Open any chapter, click floating chat button, select text, click "Ask about selected text", verify AI response displays in styled bubbles

### Backend Implementation for User Story 2

- [X] T039 [P] [US2] Create RAG embeddings service in backend/src/llm/provider.py (generate_embedding)
- [X] T040 [P] [US2] Create RAG retrieval service in backend/src/services/rag_service.py
- [X] T041 [US2] Create Gemini generation service in backend/src/llm/gemini_client.py
- [X] T042 [US2] Create chat session service in backend/src/services/rag_service.py (query method)
- [X] T043 [US2] Create /api/rag/query POST endpoint in backend/src/api/rag.py
- [X] T044 [US2] Create /api/rag/query POST endpoint (handles messages)
- [X] T045 [US2] Create /api/rag/query POST endpoint (sync, SSE not yet implemented)

### Frontend Implementation for User Story 2

- [X] T046 [P] [US2] Create ChatWidget floating button component in frontend/src/components/ChatBot/ChatBot.tsx
- [X] T047 [P] [US2] Create ChatModal (integrated in ChatBot.tsx as widget panel)
- [X] T048 [P] [US2] Create MessageBubble component (integrated in ChatBot.tsx)
- [X] T049 [P] [US2] Create TypingIndicator animation component (integrated in ChatBot.tsx)
- [X] T050 [P] [US2] Create TextSelectionButton component in frontend/src/components/ChatSelection.tsx
- [X] T051 [US2] Create useTextSelection hook (integrated in ChatSelection.tsx)
- [X] T052 [US2] Create chat API client service (integrated in ChatBot.tsx fetch calls)
- [X] T053 [US2] Create ChapterContextIndicator (integrated as selectionIndicator in ChatBot.tsx)
- [X] T054 [US2] Integrate ChatWidget into Docusaurus theme layout in frontend/src/theme/DocItem/Layout/index.tsx

### Content Indexing for User Story 2

- [X] T055 [US2] Create content indexing script for Qdrant in backend/src/services/indexing_service.py
- [ ] T056 [US2] Index sample chapter content into Qdrant collection

**Checkpoint**: RAG chatbot fully functional with text selection context - User Story 2 complete

---

## Phase 5: User Story 3 - User Authentication (Priority: P3)

**Goal**: Better-Auth signup/signin with profile collection (software/hardware background, skill level, language preference)

**Independent Test**: Click Sign Up, complete form, verify profile setup modal appears, complete profile, verify signin works

### Backend Implementation for User Story 3

- [X] T057 [US3] Create auth service in backend/src/auth/oauth.py, jwt_handler.py
- [X] T058 [US3] Create /api/auth/signup POST endpoint in backend/src/api/auth.py
- [X] T059 [US3] Create /api/auth/signin POST endpoint in backend/src/api/auth.py (login)
- [X] T060 [US3] Create /api/auth/logout POST endpoint in backend/src/api/auth.py
- [X] T061 [US3] Create /api/auth/me GET endpoint in backend/src/api/auth.py
- [X] T062 [US3] Create user profile service (integrated in personalization)
- [X] T063 [US3] Create /api/personalization/profile endpoints in backend/src/api/personalization.py
- [X] T064 [US3] Create authentication middleware in backend/src/auth/dependencies.py

### Frontend Implementation for User Story 3

- [X] T065 [P] [US3] Create AuthModal (as SignIn/SignUp modals in Auth/)
- [X] T066 [P] [US3] Create SignupForm component in frontend/src/components/Auth/SignUp.tsx
- [X] T067 [P] [US3] Create SigninForm component in frontend/src/components/Auth/SignIn.tsx
- [ ] T068 [P] [US3] Create ProfileSetup component with background questions in frontend/src/components/Auth/ProfileSetup.tsx
- [X] T069 [US3] Create useAuth hook (AuthContext) in frontend/src/components/Auth/AuthContext.tsx
- [X] T070 [US3] Create auth API client (integrated in AuthContext.tsx)
- [ ] T071 [US3] Create user API client service in frontend/src/services/user.ts
- [X] T072 [US3] Add Sign In / Sign Up buttons via UserMenu in frontend/src/components/Auth/UserMenu.tsx

**Checkpoint**: Authentication fully functional with profile setup - User Story 3 complete

---

## Phase 6: User Story 4 - Content Personalization (Priority: P4)

**Goal**: Personalize button triggers BeginnerSimplifierAgent or HardwareContextAgent based on user profile

**Independent Test**: Login as beginner user, navigate to chapter, click Personalize, verify simplified content displays

### Backend Implementation for User Story 4

- [X] T073 [P] [US4] Create base Agent class in backend/src/agents/__init__.py
- [ ] T074 [P] [US4] Create simplify_for_beginner skill in backend/src/services/skills/simplify_for_beginner.py
- [ ] T075 [P] [US4] Create hardware_mapping skill in backend/src/services/skills/hardware_mapping.py
- [X] T076 [US4] Create BeginnerSimplifierAgent (as chapter_writer in backend/src/agents/chapter_writer.py)
- [ ] T077 [US4] Create HardwareContextAgent in backend/src/services/agents/hardware_context.py
- [X] T078 [US4] Create personalization service (api endpoints) in backend/src/api/personalization.py
- [X] T079 [US4] Create /api/personalization/simplify POST endpoint in backend/src/api/personalization.py
- [X] T080 [US4] Create PersonalizedContent model in backend/src/models/personalization_profile.py

### Frontend Implementation for User Story 4

- [X] T081 [US4] Create PersonalizeButton component in frontend/src/components/PersonalizeButton.tsx
- [X] T082 [US4] Create personalization API client (integrated in PersonalizeButton.tsx)
- [X] T083 [US4] Create PersonalizedContentDisplay (integrated in PersonalizeButton.tsx)
- [X] T084 [US4] Integrate PersonalizeButton into chapter MDX template (via DocItem swizzle)

**Checkpoint**: Content personalization fully functional - User Story 4 complete

---

## Phase 7: User Story 5 - Urdu Translation (Priority: P5)

**Goal**: Translate to Urdu button triggers UrduTranslationAgent, respects user language preference

**Independent Test**: Navigate to chapter, click Translate to Urdu, verify Urdu content displays, click Show Original to revert

### Backend Implementation for User Story 5

- [X] T085 [P] [US5] Create urdu_translate skill in backend/src/agents/translation_skill.py
- [X] T086 [US5] Create UrduTranslationAgent (integrated in translation_service.py)
- [X] T087 [US5] Create /api/translation/translate POST endpoint in backend/src/api/translation.py
- [X] T088 [US5] Add translation caching to TranslationCache model in backend/src/models/translation_cache.py

### Frontend Implementation for User Story 5

- [X] T089 [US5] Create TranslateButton component in frontend/src/components/TranslateUrdu.tsx
- [X] T090 [US5] Create TranslatedContentDisplay (integrated in TranslateUrdu.tsx)
- [X] T091 [US5] Add RTL CSS support for Urdu in frontend/src/css/custom.css (.urdu-content class)
- [X] T092 [US5] Integrate TranslateButton into chapter MDX template (via DocItem swizzle)

**Checkpoint**: Urdu translation fully functional - User Story 5 complete

---

## Phase 8: Additional AI Agents & Skills (Bonus)

**Purpose**: Implement remaining agents and skills for bonus points

- [ ] T093 [P] Create PhysicalAIInstructor agent in backend/src/services/agents/physical_ai_instructor.py
- [ ] T094 [P] Create EmbodiedIntelligenceAgent in backend/src/services/agents/embodied_intelligence.py
- [ ] T095 [P] Create real_world_robot_example skill in backend/src/services/skills/real_world_robot_example.py
- [ ] T096 [P] Create exam_ready_summary skill in backend/src/services/skills/exam_ready_summary.py
- [X] T097 [P] Create context_only_answer skill (integrated in rag_service.py system prompt)
- [X] T098 Integrate context_only_answer skill into RAG chatbot (in rag_service.py _generate_answer)

**Checkpoint**: All 5 agents and 6 skills implemented

---

## Phase 9: Deployment & Polish

**Purpose**: Production deployment and cross-cutting improvements

### Deployment

- [X] T099 Configure Vercel deployment for frontend in frontend/vercel.json
- [X] T100 [P] Configure Render/Railway deployment for backend in backend/render.yaml, railway.json
- [X] T101 [P] Set up environment variables in Vercel dashboard
- [X] T102 [P] Set up environment variables in Render/Railway dashboard
- [ ] T103 Configure GitHub Actions CI/CD in .github/workflows/deploy.yml
- [X] T104 Create production build and test deployment

### Polish

- [X] T105 [P] Add accessibility attributes (ARIA labels) to interactive components (ChatBot)
- [X] T106 [P] Add responsive breakpoints for mobile/tablet (CSS modules with media queries)
- [ ] T107 Run Lighthouse audit and fix performance issues
- [X] T108 Add loading states (typing indicator, button loading states)
- [X] T109 Add error boundary components (error handling in ChatBot, API calls)
- [ ] T110 Validate all components against design system tokens
- [ ] T111 Run quickstart.md validation to verify setup instructions

**Checkpoint**: Production-ready deployment complete

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - Frontend only, no backend needed
- **User Story 2 (Phase 4)**: Depends on Foundational - Requires backend RAG infrastructure
- **User Story 3 (Phase 5)**: Depends on Foundational - Requires backend auth infrastructure
- **User Story 4 (Phase 6)**: Depends on US3 (needs auth for user profile)
- **User Story 5 (Phase 7)**: Depends on US4 (shares personalization infrastructure)
- **Bonus Agents (Phase 8)**: Depends on US2 (RAG) and US4 (agents base)
- **Deployment (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

```
US1 (Landing Page) ──────────────────────────────────────► Standalone (MVP)
                                                              │
US2 (Chatbot) ───────────────────────────────────────────────┤
                                                              │
US3 (Auth) ──────────────────────────────────────────────────┤
        │                                                     │
        └──► US4 (Personalization) ───────────────────────────┤
                    │                                         │
                    └──► US5 (Translation) ───────────────────┘
```

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T010)
- All Foundational models can run in parallel (T024-T028)
- All design system base components can run in parallel (T012-T014)
- Within US1: All landing components can run in parallel (T029-T033)
- Within US2: All chatbot UI components can run in parallel (T046-T050)
- Within US3: All auth UI components can run in parallel (T065-T068)
- Within US4: Agent skills can run in parallel (T074-T075)
- Within Phase 8: All bonus agents/skills can run in parallel (T093-T097)
- Deployment tasks can run in parallel (T100-T102)

---

## Parallel Example: User Story 1

```bash
# Launch all landing page components together:
Task: "Create Hero component in frontend/src/components/landing/Hero.tsx"
Task: "Create KnowledgeCard component in frontend/src/components/landing/KnowledgeCard.tsx"
Task: "Create CourseRoadmap component in frontend/src/components/landing/CourseRoadmap.tsx"
Task: "Create Navbar component in frontend/src/components/landing/Navbar.tsx"
Task: "Create Footer component in frontend/src/components/landing/Footer.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (design system + backend foundation)
3. Complete Phase 3: User Story 1 (Landing Page)
4. **STOP and VALIDATE**: Test landing page independently
5. Deploy to Vercel for demo

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test RAG chatbot → Deploy/Demo
4. Add User Story 3 → Test auth flow → Deploy/Demo
5. Add User Story 4 → Test personalization → Deploy/Demo
6. Add User Story 5 → Test translation → Deploy/Demo
7. Add Bonus Agents → Final polish → Production deployment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Frontend Landing)
   - Developer B: User Story 2 Backend (RAG)
   - Developer C: User Story 3 Backend (Auth)
3. Then:
   - Developer A: User Story 2 Frontend (Chatbot UI)
   - Developer B: User Story 4 (Personalization)
   - Developer C: User Story 3 Frontend (Auth UI)
4. Finally:
   - All: User Story 5, Bonus Agents, Deployment

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Summary

| Phase | Tasks | Completed | Remaining |
|-------|-------|-----------|-----------|
| Setup | 10 | 9 | 1 |
| Foundational | 18 | 18 | 0 |
| US1 - Landing | 10 | 10 | 0 |
| US2 - Chatbot | 18 | 17 | 1 |
| US3 - Auth | 16 | 14 | 2 |
| US4 - Personalization | 12 | 9 | 3 |
| US5 - Translation | 8 | 8 | 0 |
| Bonus Agents | 6 | 2 | 4 |
| Deployment | 13 | 9 | 4 |
| **Total** | **111** | **96** | **15** |

**Progress**: 86% Complete (96/111 tasks)
**MVP Scope**: Phases 1-3 (38 tasks) - Landing page with design system ✓ COMPLETE
**Full Feature**: All phases (111 tasks)

### Remaining Tasks Summary
- T009: Configure Tailwind CSS (optional - using CSS modules)
- T056: Index sample chapter content
- T068, T071: ProfileSetup, user API client
- T074, T075, T077: Personalization skills/agents
- T093-T096: Bonus agents/skills
- T103, T107, T110, T111: CI/CD, Lighthouse, validation
