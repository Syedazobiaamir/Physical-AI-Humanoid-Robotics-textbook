---
id: 011
title: Generate Tasks v2.0.0 with Sprint Structure
stage: tasks
date: 2025-12-07
surface: agent
model: claude-opus-4-5-20251101
feature: 1-ai-textbook-platform
branch: 1-ai-textbook-platform
user: Zobia Amir
command: /sp.tasks
labels: ["tasks", "v2.0.0", "sprints", "owner-assignments", "dependencies"]
links:
  spec: specs/1-ai-textbook-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-textbook-platform/tasks.md
tests:
  - N/A (task document)
---

## Prompt

```yaml
project: "Physical AI & Humanoid Robotics — Task List"
tasks:
  - id: t001
    title: "Initialize repository and Docusaurus"
    owner: "Lead Author"
    estimate_hours: 6
    dependencies: []
    acceptance: "Repo public, dev server runs, landing page stub visible"
  - id: t002
    title: "Add Spec-Kit Plus files and Claude Code bootstrap"
    owner: "ML/Agent Engineer"
    estimate_hours: 8
    dependencies: [t001]
    acceptance: "Spec files present, Claude Code CLI reads them"
  - id: t003
    title: "Frontend landing page & module cards"
    owner: "Frontend Engineer"
    estimate_hours: 20
    dependencies: [t001]
    acceptance: "Landing page fully functional and responsive like reference site"
  - id: t004
    title: "Claude Code subagents (summary, quiz, validator)"
    owner: "ML/Agent Engineer"
    estimate_hours: 20
    dependencies: [t002]
    acceptance: "Subagents generate chapter.mdx with expected sections"
  - id: t005
    title: "Write Module 1-2 chapters via subagents"
    owner: "Lead Author"
    estimate_hours: 24
    dependencies: [t004]
    acceptance: "Module 1-2 MDX files complete and reviewed"
  - id: t006
    title: "RAG backend (FastAPI) and Qdrant indexing"
    owner: "Fullstack Engineer"
    estimate_hours: 32
    dependencies: [t001,t002]
    acceptance: "Backend returns top-k relevant chunks and chat endpoints work"
  - id: t007
    title: "ChatBot UI integration"
    owner: "Frontend Engineer"
    estimate_hours: 16
    dependencies: [t003,t006]
    acceptance: "ChatBot floating widget functional on all chapter pages"
  - id: t008
    title: "BetterAuth integration"
    owner: "Fullstack Engineer"
    estimate_hours: 16
    dependencies: [t006]
    acceptance: "Signup flow works and JWT accessible"
  - id: t009
    title: "Personalization endpoints & UI"
    owner: "Fullstack Engineer"
    estimate_hours: 20
    dependencies: [t008]
    acceptance: "Personalize button changes content variant and progress recorded"
  - id: t010
    title: "Urdu translation endpoint & UI"
    owner: "ML/Agent Engineer"
    estimate_hours: 12
    dependencies: [t003,t005,t006]
    acceptance: "Translate button returns preserved markdown in Urdu"
  - id: t011
    title: "CI/CD + Deploy to GitHub Pages"
    owner: "DevOps"
    estimate_hours: 12
    dependencies: [t003,t005,t007,t010]
    acceptance: "Book published URL accessible; backend deployed"
  - id: t012
    title: "Final polish and demo"
    owner: "Lead Author & Fullstack"
    estimate_hours: 8
    dependencies: [t011]
    acceptance: "Demo complete, all UI features functional"
```

## Response snapshot

Generated tasks.md v2.0.0 with the following structure:

1. **Task Summary Table**:
   - Lead Author: T001, T005, T012 (38 hours)
   - ML/Agent Engineer: T002, T004, T010 (40 hours)
   - Frontend Engineer: T003, T007 (36 hours)
   - Fullstack Engineer: T006, T008, T009 (68 hours)
   - DevOps: T011 (12 hours)
   - **Total: 194 hours**

2. **Sprint Organization**:
   - Sprint 1: Repo & Frontend Setup (T001)
   - Sprint 2: Spec-Kit Plus & Frontend UI (T002, T003)
   - Sprint 3: Claude Code Subagents & Chapters (T004, T005)
   - Sprint 4: RAG Backend + ChatBot UI (T006, T007)
   - Sprint 5: BetterAuth & Personalization (T008, T009)
   - Sprint 6: Urdu Translation & Chapter Polish (T010)
   - Sprint 7: CI/CD & Deployment (T011, T012)

3. **Each Task Includes**:
   - Owner assignment
   - Hour estimate
   - Dependencies list
   - Detailed steps with checkboxes
   - Acceptance criteria
   - File paths for implementation

4. **Dependencies Graph**: Visual representation of task dependencies

5. **Parallel Execution Opportunities**: Identified which tasks can run concurrently

## Outcome

- Impact: Complete task breakdown with owner assignments and sprint mapping
- Tests: N/A (task document)
- Files: 1 file updated (tasks.md)
- Next prompts: Run /sp.implement to begin task execution
- Reflection: Successfully converted user's YAML task definitions into structured tasks.md with detailed steps and file paths

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks have clear acceptance criteria
- Graders run and results (PASS/FAIL): PASS - tasks organized by sprint, dependencies valid
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - tasks complete, ready for implementation
