<!--
Sync Impact Report:
- Version change: 3.0.0 → 4.0.0
- Bump rationale: MAJOR - Principles redefined with new names and scope:
  1. "Spec-Driven Development" → retained with UIUX Theme Addendum reference
  2. "AI-First Authoring" → "AI-First Design" with skill/subagent emphasis
  3. "Modular, Reusable Intelligence" → merged into AI-First Design
  4. "Production-Grade UI/UX" → "Single Unified Theme" with Dark Blue + Yellow brand
  5. "Accessibility & Performance" → "Performance & Accessibility" reordered
  6. NEW: "User Trust & Safety" added as distinct principle
- Modified sections:
  - Project Name: "Physical AI & Humanoid Robotics Course" → "AI-Native Technical Textbook Platform"
  - Mission: Updated to emphasize skill-based chatbot architecture
  - Vision: Restructured with unified theme and trust/safety focus
  - Core Principles: Completely reorganized (5 principles with new definitions)
- Added sections:
  - User Trust & Safety principle (authentication, AI limitations, data transparency)
  - UIUX Theme Addendum reference in Spec-Driven Development
- Removed sections:
  - Modular, Reusable Intelligence (merged into AI-First Design)
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ No changes needed (generic Constitution Check)
  - .specify/templates/spec-template.md: ✅ No changes needed (requirements structure generic)
  - .specify/templates/tasks-template.md: ✅ No changes needed (task structure generic)
- Follow-up TODOs:
  - Create UIUX Theme Addendum document if not exists
-->
# AI-Native Technical Textbook Platform — Project Constitution

## Project Metadata

**Name**: AI-Native Technical Textbook Platform
**Version**: 4.0.0

### Owners

| Name | Role |
|------|------|
| Zobia Amir | Lead Author & Designer |
| Panaversity Hackathon Team | Review & Infrastructure |

### Mission

**Short**: Build an AI-native technical textbook platform that teaches Physical AI & Humanoid Robotics using interactive content and embedded AI skills.

**Long**: Create a world-class educational platform featuring interactive content, embedded AI skills, reusable subagents, personalization, and multilingual access. The chatbot MUST provide functionality through reusable skills and subagents rather than operating as a fully autonomous agent, ensuring predictable and controlled AI interactions.

## Vision

Build an AI-Native Technical Textbook Platform that teaches Physical AI & Humanoid Robotics with:

- **Single Unified Theme**: Dark Blue + Yellow brand system with consistent visual identity across Landing Page, Book, Auth, Chatbot, and Dashboard
- **AI-First Interactions**: Every major user interaction leverages AI skills with chatbot functionality delivered through reusable skills and subagents
- **Spec-Driven Quality**: No feature without a specification; UI/UX governed by the UIUX Theme Addendum
- **User Trust & Safety**: Secure authentication, clear AI limitations, and transparent data usage
- **Performance & Accessibility**: Fast load times, keyboard accessible, and mobile responsive

### Scope

**In Scope**:
- Docusaurus book content (Modules 1-4 + Capstone + Appendices)
- Spec-Kit Plus specifications for all chapters
- Reusable AI skills and subagents (quiz generator, summarizer, validator, translator)
- RAG backend: FastAPI, Qdrant, Neon Postgres (user metadata)
- Frontend: Docusaurus MDX components, ChatKit widget, personalization and Urdu toggle
- Unified theme implementation: Dark Blue + Yellow across all components
- Authentication integration with Clerk for Signup/Signin
- Deployment: Vercel for frontend, serverless functions for backend

**Out of Scope**:
- Building custom hardware
- Purchasing robots
- Fully autonomous chatbot agents (skills and subagents only)

## Core Principles

### I. Single Unified Theme

The platform MUST implement a Dark Blue + Yellow brand system with consistent visual identity across ALL user-facing components. This includes the Landing Page, Book/Documentation, Authentication flows, Chatbot interface, and Dashboard. No component MAY deviate from the established design system. All UI/UX decisions MUST reference and comply with the UIUX Theme Addendum document.

**Requirements**:
- Dark Blue (#1a1a2e or similar) as primary background/accent color
- Yellow (#ffd700 or similar) as highlight/action color
- Consistent typography, spacing, and component styling
- Unified iconography and visual language
- Same visual identity in light/dark mode variants

### II. AI-First Design

Every major user interaction MUST leverage AI skills. The chatbot MUST provide functionality through reusable skills and subagents, NOT as a fully autonomous agent. This ensures predictable behavior, maintainable code, and clear boundaries for AI capabilities.

**Requirements**:
- AI skills MUST be modular and independently testable
- Subagents MUST have defined inputs, outputs, and error handling
- User-facing AI interactions MUST have clear capability boundaries
- AI features MUST gracefully degrade when services are unavailable
- Skills include: quiz generation, content summarization, translation, validation

### III. Spec-Driven Development

No feature MAY be implemented without a formal specification. All development MUST follow the Spec-Kit Plus methodology with formal specifications (specs), implementation plans (plan), and testable tasks (tasks). UI/UX decisions MUST be governed by the UIUX Theme Addendum to ensure design consistency.

**Requirements**:
- Every feature MUST have spec.md before implementation begins
- UI components MUST reference UIUX Theme Addendum for styling decisions
- Changes to visual design MUST update the addendum first
- Specifications MUST include acceptance criteria and test scenarios

### IV. User Trust & Safety

The platform MUST prioritize user trust through secure authentication, clear communication of AI limitations, and transparent data usage policies. Users MUST understand what AI can and cannot do, and how their data is used.

**Requirements**:
- Authentication MUST use secure, industry-standard methods (Clerk)
- AI limitations MUST be clearly communicated to users
- Data collection and usage MUST be transparent and documented
- User consent MUST be obtained for data processing
- Error messages MUST be helpful without exposing sensitive information
- No hardcoded secrets or tokens in source code

### V. Performance & Accessibility

The platform MUST deliver fast load times, keyboard accessibility, and mobile responsiveness. All users, regardless of device or ability, MUST have full access to platform functionality.

**Requirements**:
- Page load time MUST be under 3 seconds on standard connections
- All interactive elements MUST be keyboard accessible
- Mobile responsive design MUST work on screens 320px and wider
- WCAG 2.1 AA compliance for accessibility standards
- Images MUST have alt text; videos MUST have captions where applicable
- Urdu translation support for multilingual accessibility

## Governance

This constitution supersedes all other development practices. All PRs and reviews MUST verify compliance with these principles.

### Development Guidelines

1. **Specs before code**: All features MUST be defined via specs before implementation
2. **Theme compliance**: All UI components MUST comply with UIUX Theme Addendum
3. **Skills over autonomy**: Chatbot MUST use defined skills, not autonomous decision-making
4. **Security by default**: All user data handling MUST follow security best practices
5. **Cloud deployment strategy**: Frontend on Vercel; backend via serverless functions

### Amendment Procedure

1. Amendments require formal documentation
2. Team approval required for all changes
3. Migration plan MUST accompany breaking changes
4. UIUX Theme Addendum MUST be updated before any visual changes
5. Complexity MUST be justified with clear value proposition

### Versioning Policy

- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

**Version**: 4.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-15
