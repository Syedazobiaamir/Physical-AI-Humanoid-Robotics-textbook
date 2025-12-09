---
id: 014
title: Remove Duplicate Chatbot and Setup Deployment Config
stage: green
date: 2025-12-09
surface: agent
model: claude-opus-4-5-20251101
feature: 1-ai-textbook-platform
branch: main
user: GibTek
command: /sp.implement
labels: ["chatbot", "deployment", "vercel", "config", "cleanup"]
links:
  spec: specs/1-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/ChatWidget.tsx (deleted)
  - frontend/src/components/ChatSelection.tsx (simplified)
  - frontend/src/components/index.ts (updated)
  - frontend/src/config/api.ts (created)
  - frontend/src/components/ChatBot/ChatBot.tsx (updated)
  - frontend/src/components/ChapterQuiz.tsx (updated)
  - frontend/src/components/TranslateUrdu.tsx (updated)
  - frontend/src/components/PersonalizeButton.tsx (updated)
  - frontend/src/components/Auth/AuthProvider.tsx (updated)
  - frontend/src/services/auth.js (updated)
tests:
  - Build test passed (npm run build)
---

## Prompt

in my book their is two chatbot delete previous one and i have deploy my frontend in vercel but how to deploy frontend and where deploy and connected to fronted that work properly

## Response snapshot

Identified and resolved the duplicate chatbot issue:
1. Found 3 chatbot components: ChatBot, ChatWidget, ChatSelection
2. Deleted unused ChatWidget.tsx
3. Simplified ChatSelection.tsx to only emit selection events (removed duplicate floating button)
4. ChatBot.tsx remains as the single chatbot UI

Created centralized API configuration:
1. Created frontend/src/config/api.ts with environment-aware URL switching
2. Updated all 7 components to use centralized config instead of hardcoded localhost URLs
3. Frontend build passes successfully

Provided deployment instructions for backend:
- Railway (recommended)
- Render
- Fly.io
- Instructions to update PRODUCTION_API_URL after deployment

## Outcome

- ✅ Impact: Removed UI duplication (was showing 2 chatbot buttons), centralized API config for easy production deployment
- 🧪 Tests: Build passed (npm run build completed successfully)
- 📁 Files: 10 files modified/created, 1 file deleted
- 🔁 Next prompts: Deploy backend to Railway/Render/Fly.io, then update PRODUCTION_API_URL
- 🧠 Reflection: The duplicate issue was caused by both ChatSelection and ChatBot having their own floating buttons - simplified by making ChatSelection event-only

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward refactoring
- Graders run and results (PASS/FAIL): Build PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Deploy backend and verify chatbot connectivity end-to-end
