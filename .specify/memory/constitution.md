<!--
Sync Impact Report:
- Version change: N/A (initial version) → 1.1.0
- Added sections: Core Principles (6), Additional Constraints, Development Workflow
- Templates requiring updates: N/A (initial creation)
- Follow-up TODOs: RATIFICATION_DATE (to be set when constitution is formally adopted)
-->
# Physical AI & Humanoid Robotics — AI-Native Textbook Project Constitution

## Core Principles

### I. AI-Native Development (NON-NEGOTIABLE)
All textbook content and platform features must leverage AI tools and automation from the ground up. This includes using Claude Code and Spec-Kit Plus for chapter generation, quiz creation, and reusable agent skills. Every feature should demonstrate the power of AI in educational content creation and delivery.

### II. Spec-Driven Development
All development must follow the Spec-Kit Plus methodology with formal specifications (specs), implementation plans (plan), and testable tasks (tasks). Each chapter must have a formal spec before implementation, ensuring consistent quality and comprehensive coverage of Physical AI & Humanoid Robotics concepts.

### III. Accessibility & Internationalization
The textbook platform must be accessible to diverse audiences, including support for Urdu translation and personalized content adaptation. All content and features must be designed with inclusivity in mind, enabling global reach and diverse learning preferences.

### IV. Production-Ready Architecture
The Docusaurus book, RAG chatbot backend (FastAPI + Qdrant), and authentication system (BetterAuth) must be built to production standards. This includes proper error handling, performance optimization, security measures, and CI/CD deployment to GitHub Pages.

### V. Test-First Approach (NON-NEGOTIABLE)
TDD is mandatory: Tests written → User approved → Tests fail → Then implement. All features including chapters, quizzes, personalization, and translation functionality must have comprehensive test coverage before implementation. Red-Green-Refactor cycle strictly enforced.

### VI. Integration & Interoperability
Focus on seamless integration between components: Docusaurus frontend, RAG backend, authentication system, and personalization features. All system boundaries must have proper contract testing and error handling to ensure robust functionality.

## Additional Constraints
Technology stack requirements: Docusaurus for documentation, FastAPI + Qdrant for RAG backend, Neon Postgres for user metadata, BetterAuth for authentication, GitHub Actions for CI/CD. Must use Qdrant Cloud Free Tier for vectors and be runnable from public GitHub repository. Submission deadline is 2025-11-30T18:00:00+05:00.

## Development Workflow
All features must follow the Spec-Kit Plus workflow: Create spec → Generate plan → Generate tasks → Implement iteratively. Code reviews must verify compliance with all constitution principles. All chapters must include interactive quizzes, personalization features, and Urdu translation capabilities.

## Governance
This constitution supersedes all other development practices. All PRs and reviews must verify compliance with these principles. Any amendments require formal documentation, team approval, and migration plan. Complexity must be justified with clear value proposition.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-12-06
