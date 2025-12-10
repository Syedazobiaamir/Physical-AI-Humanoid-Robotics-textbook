---
id: 015
title: Deploy Backend on Vercel
stage: green
date: 2025-12-10
surface: agent
model: claude-opus-4-5-20251101
feature: 1-ai-textbook-platform
branch: main
user: GibTek
command: /sp.implement
labels: ["deployment", "vercel", "backend", "fastapi", "serverless"]
links:
  spec: specs/1-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/vercel.json
  - backend/api/index.py
  - backend/api/requirements.txt
  - backend/.vercelignore
  - backend/src/main.py
  - frontend/src/config/api.ts
  - frontend/docusaurus.config.ts
  - specs/1-ai-textbook-platform/tasks.md
tests:
  - null
---

## Prompt

i want to deploy my backend also on vercel so my chat bot also work with froontend

## Response snapshot

Configured the FastAPI backend for Vercel deployment by:

1. **Created `backend/vercel.json`** - Vercel configuration file that defines the build using `@vercel/python` runtime and routes all requests to the FastAPI app entry point.

2. **Created `backend/api/index.py`** - Serverless function entry point that properly sets up Python path and imports the FastAPI app from `src/main.py`.

3. **Created `backend/api/requirements.txt`** - Optimized dependencies for serverless (removed heavy packages like psycopg2-binary).

4. **Created `backend/.vercelignore`** - Excludes unnecessary files to reduce bundle size (tests, docs, other deployment configs).

5. **Updated `backend/src/main.py`** - Added import flexibility to work both locally and on Vercel, plus CORS configuration for Vercel domains.

6. **Updated `frontend/src/config/api.ts`** - Added dynamic API URL configuration using Docusaurus customFields and environment variables.

7. **Updated `frontend/docusaurus.config.ts`** - Added customFields for apiBaseUrl configuration.

8. **Updated `specs/1-ai-textbook-platform/tasks.md`** - Added Vercel deployment guide with step-by-step instructions.

## Outcome

- ✅ Impact: Backend configured for Vercel serverless deployment
- 🧪 Tests: None added (deployment configuration)
- 📁 Files: 8 files modified/created
- 🔁 Next prompts: Deploy backend to Vercel manually following the guide in tasks.md
- 🧠 Reflection: Vercel's zero-config FastAPI support simplifies deployment, but the nested `src/` structure required a custom entry point

## Evaluation notes (flywheel)

- Failure modes observed: None - successful configuration
- Graders run and results (PASS/FAIL): N/A - manual deployment required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test actual deployment on Vercel to verify configuration works
