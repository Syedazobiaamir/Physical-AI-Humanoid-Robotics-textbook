---
id: 010
title: Update Plan v2.0.0 with Sprint Structure
stage: plan
date: 2025-12-07
surface: agent
model: claude-opus-4-5-20251101
feature: 1-ai-textbook-platform
branch: 1-ai-textbook-platform
user: Zobia Amir
command: /sp.plan
labels: ["plan", "v2.0.0", "sprints", "frontend-ui", "architecture"]
links:
  spec: specs/1-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-textbook-platform/plan.md
  - specs/1-ai-textbook-platform/research.md
  - specs/1-ai-textbook-platform/data-model.md
  - specs/1-ai-textbook-platform/contracts/api-contracts.md
  - specs/1-ai-textbook-platform/quickstart.md
  - CLAUDE.md
tests:
  - N/A (planning document)
---

## Prompt

```yaml
project: "Physical AI & Humanoid Robotics Textbook — Plan"
timeline_overview:
  total_sprints: 7
  sprint_length_weeks: 2
  deadline: "2025-11-30T18:00:00+05:00"
sprints:
  - id: sprint-1
    name: "Repo & Frontend Setup"
    goals:
      - "Initialize Git repo and Docusaurus skeleton"
      - "Add landing page hero and basic theme"
      - "Add Part 14 folder and chapter stubs"
      - "Add Spec-Kit Plus baseline files"
    deliverables:
      - "Public repo with Docusaurus config, sample chapter, landing page hero"
  - id: sprint-2
    name: "Frontend Module Cards & Animations"
    goals:
      - "Implement module cards with hover animation"
      - "Add icons, colors, logos, favicon"
      - "Ensure mobile responsiveness"
    deliverables:
      - "Landing page + modules match reference UI"
  - id: sprint-3
    name: "Claude Code Subagents & Chapters"
    goals:
      - "Generate Module 1-2 chapters via subagents"
      - "Implement summary, quiz, validator skills"
    deliverables:
      - "MDX files for Weeks 1-7"
  - id: sprint-4
    name: "RAG Backend + ChatBot UI"
    goals:
      - "FastAPI backend, Qdrant indexing, ChatBot integration"
      - "Selection & context mode implemented"
    deliverables:
      - "ChatBot floating widget functional"
  - id: sprint-5
    name: "BetterAuth & Personalization"
    goals:
      - "Signup/Signin via BetterAuth"
      - "Per-chapter Personalize button"
    deliverables:
      - "Profile stored in Neon, personalized content returned"
  - id: sprint-6
    name: "Urdu Translation & Chapter Polish"
    goals:
      - "Add Translate button with LLM backend"
      - "Fix frontend chapter layout, images, icons, animations"
    deliverables:
      - "Chapters fully functional with personalization, translation, ChatBot"
  - id: sprint-7
    name: "CI/CD & Deployment"
    goals:
      - "GitHub Actions build + deploy"
      - "Backend deployed with Docker"
      - "Demo video preparation"
    deliverables:
      - "Publicly hosted book URL and submission ready"
```

## Response snapshot

Updated the implementation plan to v2.0.0 with the following:

1. **Plan Structure**:
   - Technical Context: TypeScript 5.x + Python 3.11, Docusaurus + FastAPI
   - Constitution Check: All 6 principles verified and passed
   - Project Structure: Web application pattern (frontend/ + backend/)
   - Sprint Overview: 7 sprints mapped to user's timeline

2. **Phase 0 Complete (research.md)**:
   - Added Frontend UI research section for reference site analysis
   - Documented animation best practices
   - Technology decisions preserved from v1

3. **Phase 1 Complete**:
   - data-model.md: Added Module entity for landing page cards
   - api-contracts.md: Added GET /api/v1/modules endpoint
   - quickstart.md: Updated with v2.0.0 frontend component notes

4. **Agent Context Updated**:
   - CLAUDE.md updated with technology stack from plan

5. **Files Updated**:
   - plan.md (complete rewrite with v2.0.0 structure)
   - research.md (added v2.0.0 frontend research)
   - data-model.md (added Module entity)
   - api-contracts.md (added modules endpoint)
   - quickstart.md (added v2.0.0 notes)

## Outcome

- Impact: MAJOR plan update with 7-sprint timeline and complete technical architecture
- Tests: N/A (planning document)
- Files: 6 files modified
- Next prompts: Run /sp.tasks to generate implementation tasks from plan
- Reflection: Successfully incorporated user's sprint structure into formal plan with Phase 0 and Phase 1 artifacts updated for v2.0.0

## Evaluation notes (flywheel)

- Failure modes observed: None - all phases completed successfully
- Graders run and results (PASS/FAIL): PASS - constitution check verified, all artifacts updated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - plan complete, ready for tasks generation
