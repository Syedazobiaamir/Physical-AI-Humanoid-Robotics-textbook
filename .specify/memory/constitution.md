<!--
Sync Impact Report:
- Version change: 2.0.0 → 3.0.0
- Bump rationale: MAJOR - Restructured principles from 6 to 5, updated
  deployment strategy from GitHub Pages to Vercel, removed NON-NEGOTIABLE markers
- Modified sections:
  - Project Name: "Physical AI & Humanoid Robotics — AI-Native Textbook Project" → "Physical AI & Humanoid Robotics Course"
  - Vision: Restructured with new emphasis areas (world-class UI/UX, animated frontend, RAG chatbot)
  - Core Principles: Reduced from 6 to 5 with new naming and scope:
    - "AI-Native Development" → "AI-First Authoring"
    - "Spec-Driven Development" → retained
    - "Accessibility & Internationalization" → "Accessibility & Performance"
    - "Production-Ready Architecture" → "Production-Grade UI/UX"
    - "Test-First Approach" → merged into other principles
    - "Integration & Interoperability" → "Modular, Reusable Intelligence"
  - Deployment Strategy: GitHub Pages → Vercel (frontend), serverless functions for backend
- Added sections:
  - Explicit Vision section with bullet points
- Removed sections:
  - Additional Constraints (merged into relevant sections)
  - Success Metrics table (simplified)
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ No changes needed (uses generic Constitution Check placeholder)
  - .specify/templates/spec-template.md: ✅ No changes needed (requirements structure is generic)
  - .specify/templates/tasks-template.md: ✅ No changes needed (test-first approach preserved in generic form)
- Follow-up TODOs: None (all placeholders resolved)
-->
# Physical AI & Humanoid Robotics Course — Project Constitution

## Project Metadata

**Name**: Physical AI & Humanoid Robotics Course
**Version**: 3.0.0

### Owners

| Name | Role |
|------|------|
| Zobia Amir | Lead Author & Designer |
| Panaversity Hackathon Team | Review & Infrastructure |

### Mission

**Short**: Create a professional, animated, AI-native course platform for Physical AI & Humanoid Robotics.

**Long**: Build a world-class Docusaurus-based interactive textbook with animated, robotics-inspired frontend design, an embedded intelligent RAG chatbot for contextual learning assistance, personalized multilingual support (English and Urdu), and full cloud deployment on Vercel.

## Vision

Create a professional, animated, AI-native textbook using Docusaurus with:

- **World-class UI/UX**: Modern, intuitive interface with professional design standards
- **Animated, robotics-inspired frontend**: Dynamic visuals and animations that reflect the Physical AI theme
- **Embedded intelligent RAG chatbot**: Context-aware AI assistant powered by Qdrant vector search and FastAPI backend
- **Personalized, multilingual learning**: Adaptive content personalization with English and Urdu language support
- **Full deployment on Vercel**: Frontend hosted on Vercel with serverless functions or alternative backend infrastructure

### Scope

**In Scope**:
- Docusaurus book content (Modules 1-4 + Capstone + Appendices)
- Spec-Kit Plus specifications for all chapters
- Claude Code subagents and reusable skills (quiz generator, summarizer, validator)
- RAG backend: FastAPI, Qdrant, Neon Postgres (user metadata)
- Frontend: Docusaurus MDX components, ChatKit widget, personalization and Urdu toggle
- Modern landing page UI: hero section, animated module cards, responsive design, icons, animations
- Authentication integration for Signup/Signin
- Deployment: Vercel for frontend, serverless functions or alternative for backend

**Out of Scope**:
- Building custom hardware
- Purchasing robots

## Core Principles

### I. Spec-Driven Development

All development MUST follow the Spec-Kit Plus methodology with formal specifications (specs), implementation plans (plan), and testable tasks (tasks). Each chapter and feature MUST have a formal spec before implementation. This ensures consistent quality, traceability, and comprehensive coverage of Physical AI & Humanoid Robotics concepts across the entire platform.

### II. AI-First Authoring

All textbook content and platform features MUST leverage Claude Code and AI automation from the ground up. This includes using AI tools for chapter generation, quiz creation, content summarization, translation, and reusable agent skills. Every component MUST demonstrate the power of AI in educational content creation and delivery, reflecting the AI-native nature of the platform.

### III. Modular, Reusable Intelligence

Platform components MUST be designed as modular, reusable units that can operate independently and integrate seamlessly. This applies to AI skills (quiz generators, summarizers, validators), frontend components (ChatKit widget, personalization buttons), and backend services (RAG pipeline, authentication). System boundaries MUST have proper contract definitions and error handling.

### IV. Production-Grade UI/UX

The Docusaurus book and all frontend components MUST meet production-grade standards for visual design and user experience. This includes professional animated interfaces, responsive layouts, consistent styling, accessibility compliance, and performance optimization. The UI/UX MUST match or exceed modern reference implementations with smooth animations and intuitive interactions.

### V. Accessibility & Performance

The platform MUST be accessible to diverse global audiences with support for Urdu translation and personalized content adaptation. All features MUST be designed with inclusivity in mind. Performance MUST meet production standards: fast page loads, optimized assets, responsive interactions, and efficient backend operations. The platform MUST be fully functional on Vercel deployment.

## Governance

This constitution supersedes all other development practices. All PRs and reviews MUST verify compliance with these principles.

### Development Guidelines

1. **Specs before code**: All features MUST be defined via specs before implementation
2. **UI/UX consistency**: Maintain visual and interaction consistency across book and frontend components
3. **Security & privacy by default**: All user data handling MUST follow security best practices; no hardcoded secrets
4. **Cloud deployment strategy**: Frontend on Vercel; backend via serverless functions or alternative cloud services

### Amendment Procedure

1. Amendments require formal documentation
2. Team approval required for all changes
3. Migration plan MUST accompany breaking changes
4. Complexity MUST be justified with clear value proposition

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

**Version**: 3.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-13
