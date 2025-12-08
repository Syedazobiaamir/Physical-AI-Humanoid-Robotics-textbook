<!--
Sync Impact Report:
- Version change: 1.1.0 → 2.0.0
- Modified sections:
  - Header: Added structured metadata (owners, mission, scope, constraints, success metrics, communication)
  - Core Principles: Retained all 6 principles with minor wording updates for consistency
  - Additional Constraints: Expanded with explicit technology requirements
  - Development Workflow: Unchanged
  - Governance: Added version bump rationale
- Added sections:
  - Formal YAML-style metadata block (Owners, Mission, Scope, Constraints, Success Metrics, Communication)
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ Consistent (Constitution Check section aligns)
  - .specify/templates/spec-template.md: ✅ Consistent (requirements structure aligns)
  - .specify/templates/tasks-template.md: ✅ Consistent (test-first approach preserved)
- Follow-up TODOs: None (all placeholders resolved)
-->
# Physical AI & Humanoid Robotics — AI-Native Textbook Project Constitution

## Project Metadata

**Name**: Physical AI & Humanoid Robotics — AI-Native Textbook Project
**Version**: 2.0.0

### Owners

| Name | Role |
|------|------|
| Zobia Amir | Lead Author & Designer |
| Panaversity Hackathon Team | Review & Infrastructure |

### Mission

**Short**: Create an AI-native textbook and platform for Physical AI & Humanoid Robotics using Claude Code + Spec-Kit Plus.

**Long**: Build a production-ready Docusaurus book with modern frontend UI (like ai-native-book-iota.vercel.app), embed a RAG chatbot (Qdrant + FastAPI), implement BetterAuth signup/signin, personalization and Urdu translation buttons, and provide CI/CD for GitHub Pages deployment.

### Scope

**In Scope**:
- Docusaurus book content (Modules 1-4 + Capstone + Appendices)
- Spec-Kit Plus specs for all chapters
- Claude Code subagents & reusable skills (quiz generator, summarizer, validator)
- RAG backend: FastAPI, Qdrant, Neon Postgres (user metadata)
- Frontend: Docusaurus MDX components, ChatKit widget, personalization & Urdu toggle
- Modern landing page UI: hero, animated module cards, responsive design, icons, animations
- BetterAuth integration for Signup/Signin
- Deployment: GitHub Actions to GitHub Pages (or Vercel alternative)

**Out of Scope**:
- Building custom hardware
- Purchasing robots

### Constraints

- Submission deadline: 2025-11-30T18:00:00+05:00
- Use Qdrant Cloud Free Tier for vectors
- Use BetterAuth for authentication
- Must be runnable from public GitHub repo

### Success Metrics

| Metric | Criteria |
|--------|----------|
| Published Book URL | Public GitHub Pages link accessible |
| RAG Functional | User can select text in a chapter and ask chatbot; answer uses only selected text when requested |
| Auth Functional | Signup/Signin via BetterAuth asks software/hardware background questions |
| Personalization | Per-chapter "Personalize" button adapts content based on stored profile |
| Urdu Translation | Per-chapter "Translate to Urdu" button produces readable Urdu content |
| Frontend UI | Landing page, module cards, animations, icons, and ChatBot match reference site |

### Communication

- Channel: WhatsApp (for live presentation invite)
- Repo: GitHub public repository

## Core Principles

### I. AI-Native Development (NON-NEGOTIABLE)

All textbook content and platform features MUST leverage AI tools and automation from the ground up. This includes using Claude Code and Spec-Kit Plus for chapter generation, quiz creation, and reusable agent skills. Every feature MUST demonstrate the power of AI in educational content creation and delivery.

### II. Spec-Driven Development

All development MUST follow the Spec-Kit Plus methodology with formal specifications (specs), implementation plans (plan), and testable tasks (tasks). Each chapter MUST have a formal spec before implementation, ensuring consistent quality and comprehensive coverage of Physical AI & Humanoid Robotics concepts.

### III. Accessibility & Internationalization

The textbook platform MUST be accessible to diverse audiences, including support for Urdu translation and personalized content adaptation. All content and features MUST be designed with inclusivity in mind, enabling global reach and diverse learning preferences.

### IV. Production-Ready Architecture

The Docusaurus book, RAG chatbot backend (FastAPI + Qdrant), and authentication system (BetterAuth) MUST be built to production standards. This includes proper error handling, performance optimization, security measures, and CI/CD deployment to GitHub Pages.

### V. Test-First Approach (NON-NEGOTIABLE)

TDD is mandatory: Tests written → User approved → Tests fail → Then implement. All features including chapters, quizzes, personalization, and translation functionality MUST have comprehensive test coverage before implementation. Red-Green-Refactor cycle strictly enforced.

### VI. Integration & Interoperability

Focus on seamless integration between components: Docusaurus frontend, RAG backend, authentication system, and personalization features. All system boundaries MUST have proper contract testing and error handling to ensure robust functionality.

## Additional Constraints

Technology stack requirements:
- **Documentation**: Docusaurus
- **RAG Backend**: FastAPI + Qdrant
- **Database**: Neon Postgres (user metadata)
- **Authentication**: BetterAuth
- **CI/CD**: GitHub Actions
- **Vector Storage**: Qdrant Cloud Free Tier
- **Hosting**: GitHub Pages (or Vercel alternative)

The platform MUST be runnable from a public GitHub repository. Submission deadline is 2025-11-30T18:00:00+05:00.

## Development Workflow

All features MUST follow the Spec-Kit Plus workflow:
1. Create spec (`/sp.specify`)
2. Generate plan (`/sp.plan`)
3. Generate tasks (`/sp.tasks`)
4. Implement iteratively (`/sp.implement`)

Code reviews MUST verify compliance with all constitution principles. All chapters MUST include interactive quizzes, personalization features, and Urdu translation capabilities.

## Governance

This constitution supersedes all other development practices. All PRs and reviews MUST verify compliance with these principles.

### Amendment Procedure

1. Amendments require formal documentation
2. Team approval required for all changes
3. Migration plan MUST accompany breaking changes
4. Complexity MUST be justified with clear value proposition

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

**Version**: 2.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-07
