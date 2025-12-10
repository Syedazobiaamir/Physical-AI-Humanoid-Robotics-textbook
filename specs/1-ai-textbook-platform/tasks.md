---
description: "Task list for Physical AI & Humanoid Robotics textbook platform implementation"
version: "2.0.0"
updated: "2025-12-07"
---

# Tasks: Physical AI & Humanoid Robotics — AI-Native Textbook Platform

**Input**: Design documents from `/specs/1-ai-textbook-platform/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Version**: 2.0.0

## Task Assignment Summary

| Owner | Tasks | Total Hours |
|-------|-------|-------------|
| Lead Author | T001, T005, T012 | 38 |
| ML/Agent Engineer | T002, T004, T010 | 40 |
| Frontend Engineer | T003, T007 | 36 |
| Fullstack Engineer | T006, T008, T009 | 68 |
| DevOps | T011 | 12 |

**Total Estimated Hours**: 194

## Format: `[ID] Owner | Hours | Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **Dependencies**: Listed per task
- Include exact file paths in descriptions

---

## Sprint 1: Repo & Frontend Setup

**Duration**: 2 weeks | **Deliverables**: Public repo with Docusaurus config, sample chapter, landing page hero

### T001 - Initialize Repository and Docusaurus ✅
**Owner**: Lead Author | **Hours**: 6 | **Dependencies**: None

**Steps**:
- [x] Create GitHub repo with README
- [x] Run `npx create-docusaurus@latest frontend classic --typescript`
- [x] Add basic theme and header matching Panaversity style
- [x] Add `frontend/docs/module-1/` folder and stub MDX files
- [x] Add landing page hero placeholder in `frontend/src/pages/index.tsx`

**Acceptance**: Repo public, dev server runs at localhost:3000, landing page stub visible

---

## Sprint 2: Spec-Kit Plus & Frontend UI

**Duration**: 2 weeks | **Deliverables**: Spec files present, landing page matching reference UI

### T002 - Add Spec-Kit Plus Files and Claude Code Bootstrap ✅
**Owner**: ML/Agent Engineer | **Hours**: 8 | **Dependencies**: T001

**Steps**:
- [x] Add `.specify/` folder with templates and scripts
- [x] Add constitution.md, spec templates, plan templates, task templates
- [x] Add Claude Code CLI bootstrap scripts
- [x] Add `.specify/skills/` with chapter-writer, summary, quiz-generator, validator skills
- [x] Document usage in README.md

**Acceptance**: Spec files present in `.specify/`, Claude Code CLI reads them correctly

---

### T003 - Frontend Landing Page & Module Cards ✅
**Owner**: Frontend Engineer | **Hours**: 20 | **Dependencies**: T001

**Steps**:
- [x] Implement landing page hero with logo, tagline, call-to-action in `frontend/src/pages/index.tsx`
- [x] Create animated module cards in `frontend/src/components/ModuleCard/`
  - Title, week, icons
  - Hover animations (scale, shadow)
- [x] Add responsive layout (mobile-first)
- [x] Add favicon in `frontend/static/img/favicon.svg`
- [x] Add logo in `frontend/static/img/logo.svg`
- [x] Configure site-wide colors and fonts in `frontend/src/css/custom.css`
- [x] Add icons (use react-icons or similar)
- [x] Test on desktop and mobile

**Acceptance**: Landing page fully functional and responsive, matches reference site (ai-native-book-iota.vercel.app)

**Files**:
```
frontend/src/pages/index.tsx
frontend/src/components/Hero/Hero.tsx
frontend/src/components/ModuleCard/ModuleCard.tsx
frontend/src/css/custom.css
frontend/static/img/favicon.svg
frontend/static/img/logo.svg
```

---

## Sprint 3: Claude Code Subagents & Chapters

**Duration**: 2 weeks | **Deliverables**: MDX files for Weeks 1-7

### T004 - Claude Code Subagents (Summary, Quiz, Validator) ✅
**Owner**: ML/Agent Engineer | **Hours**: 20 | **Dependencies**: T002

**Steps**:
- [x] Create subagent `chapter-writer` that consumes spec and outputs MDX
  - Location: `.specify/skills/chapter-writer/`
- [x] Create `summary-skill` for key points extraction
  - Location: `.specify/skills/summary/`
- [x] Create `quiz-generator` for 5 MCQs + answers
  - Location: `.specify/skills/quiz-generator/`
- [x] Create `consistency-check` skill (terminology/style validation)
  - Location: `.specify/skills/validator/`
- [x] Backend agents in `backend/src/agents/` (chapter_writer.py, quiz_generator.py, translation_skill.py)

**Acceptance**: Subagents generate chapter.mdx with expected sections (objectives, theory, labs, code, quiz, resources)

---

### T005 - Write Module 1-2 Chapters via Subagents ✅
**Owner**: Lead Author | **Hours**: 24 | **Dependencies**: T004

**Steps**:
- [x] Run Claude Code to generate Week 1 MDX (ROS2 Introduction)
- [x] Run Claude Code to generate Week 2 MDX (ROS2 Nodes & Topics)
- [x] Run Claude Code to generate Week 3 MDX (ROS2 Services & Actions)
- [x] Run Claude Code to generate Week 4 MDX (Sensor Integration)
- [x] Run Claude Code to generate Week 5 MDX (Computer Vision)
- [x] Run Claude Code to generate Week 6 MDX (SLAM)
- [x] All Module 3 & 4 chapters also generated (Weeks 7-13)
- [x] Review & edit all generated content
- [x] Verify each chapter has: objectives, theory, lab tasks, code examples, quizzes, resources

**Acceptance**: Module 1-4 MDX files complete in `frontend/docs/`, reviewed and ready

---

## Sprint 4: RAG Backend + ChatBot UI

**Duration**: 2 weeks | **Deliverables**: ChatBot floating widget functional

### T006 - RAG Backend (FastAPI) and Qdrant Indexing ✅
**Owner**: Fullstack Engineer | **Hours**: 32 | **Dependencies**: T001, T002

**Steps**:
- [x] Create FastAPI backend structure in `backend/`
  - `backend/src/api/main.py` - FastAPI app entry
  - `backend/src/api/routes/chat.py` - Chat endpoints
  - `backend/requirements.txt` - Dependencies
- [x] Implement `/embed` endpoint for generating embeddings
- [x] Implement `/query` endpoint for semantic search
- [x] Implement `/chat` endpoint for RAG responses
- [x] Integrate OpenAI embeddings (text-embedding-3-small)
- [x] Integrate Qdrant client for vector storage
- [x] Implement chunking pipeline (400-600 tokens per chunk)
- [x] Implement incremental indexing for chapter updates
- [ ] Add tests for selection-based retrieval in `backend/tests/`

**Acceptance**: Backend returns top-k relevant chunks, chat endpoints work, latency < 2s local

**Files**:
```
backend/src/api/main.py
backend/src/api/routes/chat.py
backend/src/services/rag.py
backend/src/services/embeddings.py
backend/src/db/qdrant.py
backend/requirements.txt
backend/tests/test_rag.py
```

---

### T007 - ChatBot UI Integration ✅
**Owner**: Frontend Engineer | **Hours**: 16 | **Dependencies**: T003, T006

**Steps**:
- [x] Create floating ChatBot widget component in `frontend/src/components/ChatBot/`
  - Fixed position bottom-right
  - Expand/collapse toggle
  - Message history display
- [x] Implement selection mode (text selection triggers chat)
- [x] Implement context mode (general Q&A)
- [x] Show source citations in chat responses
- [x] Style widget consistent with theme (colors, fonts)
- [x] Add to all chapter pages via MDX wrapper

**Acceptance**: ChatBot floating widget functional on all chapter pages, selection and context modes work

**Files**:
```
frontend/src/components/ChatBot/ChatBot.tsx
frontend/src/components/ChatBot/ChatBot.module.css
frontend/src/components/ChatSelection.tsx
frontend/src/theme/DocItem/Layout/index.tsx (wrapper)
```

---

## Sprint 5: BetterAuth & Personalization

**Duration**: 2 weeks | **Deliverables**: Profile stored in Neon, personalized content returned

### T008 - BetterAuth Integration ✅
**Owner**: Fullstack Engineer | **Hours**: 16 | **Dependencies**: T006

**Steps**:
- [x] Install and configure auth in `backend/src/auth/`
- [x] Implement OAuth adapter (Google, GitHub providers)
- [x] Create signup flow that collects:
  - Name
  - Email
  - Role (student/author/admin)
  - Software background (beginner/intermediate/advanced)
  - Hardware background (beginner/intermediate/advanced)
- [x] Configure Neon Postgres connection for user storage (with SQLite fallback)
- [x] Implement JWT issuance and validation
- [x] Create frontend auth components in `frontend/src/components/Auth/`

**Acceptance**: Signup flow works, JWT issued and accessible, profile stored in Neon

**Files**:
```
backend/src/auth/oauth.py
backend/src/auth/jwt_handler.py
backend/src/auth/dependencies.py
backend/src/database/base.py
backend/src/models/user.py
frontend/src/components/Auth/AuthContext.tsx
frontend/src/components/Auth/AuthProvider.tsx
frontend/src/components/Auth/SignIn.tsx
frontend/src/components/Auth/SignUp.tsx
frontend/src/components/Auth/UserMenu.tsx
frontend/src/components/Auth/ProtectedRoute.tsx
```

---

### T009 - Personalization Endpoints & UI ✅
**Owner**: Fullstack Engineer | **Hours**: 20 | **Dependencies**: T008

**Steps**:
- [x] Implement `/personalize` endpoint in `backend/src/api/personalization.py`
  - Accept chapter_id and skill_level
  - Return content variants (beginner/intermediate/advanced)
- [x] Create personalization service in backend
- [x] Create `<PersonalizeButton />` component in `frontend/src/components/PersonalizeButton.tsx`
  - Button at chapter start
  - Skill level selector
  - Content replacement logic
- [x] Implement progress tracking
  - Track chapter progress
  - Track skill level preferences

**Acceptance**: Personalize button changes content variant, progress recorded

**Files**:
```
backend/src/api/personalization.py
backend/src/api/progress.py
backend/src/models/personalization_profile.py
backend/src/models/progress_tracking.py
frontend/src/components/PersonalizeButton.tsx
```

---

## Sprint 6: Urdu Translation & Chapter Polish

**Duration**: 2 weeks | **Deliverables**: Chapters fully functional with personalization, translation, ChatBot

### T010 - Urdu Translation Endpoint & UI ✅
**Owner**: ML/Agent Engineer | **Hours**: 12 | **Dependencies**: T003, T005, T006

**Steps**:
- [x] Implement `/translate` endpoint in `backend/src/api/translation.py`
  - Accept markdown content
  - Return Urdu translation preserving formatting
- [x] Create translation service in `backend/src/services/translation_service.py`
  - Preserve code blocks
  - Preserve headings
  - Handle technical terms (transliterate or glossary)
- [x] Implement translation caching
- [x] Create `<TranslateUrdu />` component in `frontend/src/components/TranslateUrdu.tsx`
  - Button on chapter pages
  - Toggle between English/Urdu

**Acceptance**: Translate button returns preserved markdown in Urdu, code blocks intact

**Files**:
```
backend/src/api/translation.py
backend/src/services/translation_service.py
backend/src/agents/translation_skill.py
backend/src/models/translation_cache.py
frontend/src/components/TranslateUrdu.tsx
```

---

## Sprint 7: CI/CD & Deployment

**Duration**: 2 weeks | **Deliverables**: Publicly hosted book URL and submission ready

### T011 - CI/CD + Deploy to GitHub Pages ✅
**Owner**: DevOps | **Hours**: 12 | **Dependencies**: T003, T005, T007, T010

**Steps**:
- [x] Create GitHub Actions workflow for frontend in `.github/workflows/frontend.yml`
  - Build Docusaurus on push to main
  - Deploy to GitHub Pages
- [x] Create GitHub Actions workflow for backend in `.github/workflows/backend.yml`
  - Build Docker image
  - Push to container registry
- [x] Dockerize backend with `backend/Dockerfile`
- [x] Add deployment configs for Railway, Render, Fly.io
- [x] Add Vercel deployment config for backend (`backend/vercel.json`, `backend/api/index.py`)
- [x] Update frontend API config for dynamic backend URL (`frontend/src/config/api.ts`)
- [ ] Deploy backend to Vercel (see deployment guide below)
- [ ] Configure environment variables for production
- [ ] Test deployed URLs and verify functionality

**Acceptance**: Book published URL accessible (GitHub Pages/Vercel), backend deployed and responsive

**Files**:
```
.github/workflows/frontend.yml
.github/workflows/backend.yml
backend/Dockerfile
backend/docker-compose.yml
backend/railway.json
backend/render.yaml
backend/fly.toml
backend/vercel.json
backend/api/index.py
backend/api/requirements.txt
backend/.vercelignore
frontend/src/config/api.ts
```

**Vercel Backend Deployment Guide**:
1. Go to [Vercel Dashboard](https://vercel.com/dashboard) > "Add New Project"
2. Import your GitHub repository
3. **Important**: Set Root Directory to `backend`
4. Vercel will auto-detect FastAPI - just click Deploy
5. After deployment, copy the URL (e.g., `https://your-project.vercel.app`)
6. Go to your **frontend** Vercel project > Settings > Environment Variables
7. Add: `DOCUSAURUS_API_BASE_URL` = `https://your-project.vercel.app/api/v1`
8. Redeploy the frontend to pick up the new environment variable
9. Test the ChatBot functionality on the live site

---

### T012 - Final Polish and Demo
**Owner**: Lead Author & Fullstack | **Hours**: 8 | **Dependencies**: T011

**Steps**:
- [ ] Verify all frontend animations work correctly
- [ ] Test ChatBot on all chapter pages
- [ ] Verify icons, module cards, and responsive design
- [ ] Test personalization flow end-to-end
- [ ] Test Urdu translation on sample chapters
- [ ] Record 90-second demo video
- [ ] Prepare submission materials

**Acceptance**: Demo complete, all UI features functional, ready for submission

---

## Dependencies Graph

```
T001 (Repo Setup)
  ├── T002 (Spec-Kit Plus) ──► T004 (Subagents) ──► T005 (Chapters)
  ├── T003 (Frontend UI) ──► T007 (ChatBot UI) ──► T011 (Deploy)
  └── T006 (RAG Backend) ──► T007 (ChatBot UI)
                          └── T008 (Auth) ──► T009 (Personalization)
                          └── T010 (Translation) ──► T011 (Deploy)

T011 (Deploy) ──► T012 (Final Polish)
```

## Parallel Execution Opportunities

| Phase | Parallel Tasks |
|-------|---------------|
| Sprint 1 | T001 alone (foundational) |
| Sprint 2 | T002 + T003 (after T001) |
| Sprint 3 | T004 alone, then T005 |
| Sprint 4 | T006 + T007 (T007 waits for T003 + T006) |
| Sprint 5 | T008 → T009 (sequential) |
| Sprint 6 | T010 (can parallel with Sprint 5) |
| Sprint 7 | T011 → T012 (sequential) |

## Notes

- Each task includes specific file paths for implementation
- Owners are assigned based on user input
- Hour estimates are from user input
- Dependencies ensure proper sequencing
- Checkboxes track step completion within each task
