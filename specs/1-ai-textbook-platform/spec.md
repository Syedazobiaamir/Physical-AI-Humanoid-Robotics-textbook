# Feature Specification: Physical AI & Humanoid Robotics — AI-Native Textbook

**Feature Branch**: `1-ai-textbook-platform`
**Created**: 2025-12-06
**Updated**: 2025-12-07
**Version**: 2.0.0
**Status**: Draft

## Overview

This specification defines the acceptance criteria for the full textbook, frontend UI, RAG chatbot, BetterAuth integration, personalization, Urdu translation, and deployment pipeline. The book follows Modules 1-4 + Capstone, Weeks 1-13.

## Components

| ID | Name | Description |
|----|------|-------------|
| frontend | Frontend UI | Landing page, module cards, chapter pages with ChatBot, personalization, Urdu translation |
| book | Docusaurus Book | Docusaurus site with MDX chapters and interactive components |
| rag | RAG Chatbot | Retrieval-augmented chatbot using Qdrant, FastAPI, ChatKit/OpenAI Agents |
| auth | BetterAuth Integration | Signup and Signin flows with background capture |
| personalization | Personalization Engine | Generates learning path and content adaptations per user profile |
| urdu | Urdu Translation | On-demand Urdu translation using LLM, preserving formatting |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Modern Landing Page (Priority: P1)

User visits the textbook platform and sees a modern, engaging landing page with a hero section, animated module cards, and clear navigation. The design matches the reference site (ai-native-book-iota.vercel.app) with responsive layout, consistent styling, and professional icons.

**Why this priority**: The landing page is the first impression and determines user engagement. A polished UI builds credibility for the educational content.

**Independent Test**: User can navigate to the landing page, see the hero section, browse animated module cards, and access the textbook content. The design is responsive across desktop and mobile devices.

**Acceptance Scenarios**:

1. **Given** user navigates to the platform URL, **When** the page loads, **Then** a hero section with title, description, and call-to-action is displayed
2. **Given** user views the landing page, **When** user hovers over module cards, **Then** cards display animated hover effects with title, week, and icon
3. **Given** user accesses the platform on mobile, **When** page renders, **Then** layout is responsive and all elements are accessible

---

### User Story 2 - Read Interactive Textbook Content (Priority: P1)

Student accesses the Physical AI & Humanoid Robotics textbook to learn about ROS2, Gazebo/Unity, Isaac, and VLA modules. Each chapter includes learning objectives, theory, lab tasks, code examples, and quizzes. Interactive components (Personalize, TranslateUrdu, ChatSelection) are embedded in chapter pages.

**Why this priority**: This is the core value proposition - providing educational content students can access and learn from.

**Independent Test**: Student can navigate to any chapter, read the content, and interact with embedded components. The chapter content follows the weekly breakdown structure and includes all required elements.

**Acceptance Scenarios**:

1. **Given** student accesses the textbook platform, **When** student navigates to a chapter, **Then** the chapter displays learning objectives, theory, lab tasks, code examples, and quizzes
2. **Given** student is reading a chapter, **When** student interacts with MDX components, **Then** Personalize, TranslateUrdu, and ChatSelection components function correctly
3. **Given** student accesses the deployment URL, **When** student navigates any page, **Then** the page loads correctly from GitHub Pages or Vercel

---

### User Story 3 - Ask Questions Using RAG Chatbot (Priority: P2)

Student uses the floating ChatBot widget (bottom-right corner) to ask questions. In selection mode, student can select text and get answers constrained to that selection. In context mode, the chatbot retrieves relevant chunks from the full textbook.

**Why this priority**: This enhances learning by providing immediate, contextual answers to student questions.

**Independent Test**: Student can open the ChatBot, select text, ask questions, and receive accurate answers. Response latency meets performance targets.

**Acceptance Scenarios**:

1. **Given** student is reading a chapter, **When** student selects text and asks a question in selection mode, **Then** the answer is constrained to the selected text only
2. **Given** student opens the ChatBot, **When** student asks a general question in context mode, **Then** the response uses top-5 retrieved chunks with citations
3. **Given** student submits a query, **When** the system processes it, **Then** response time is under 2 seconds for local dev and under 500ms for cloud retrieval

---

### User Story 4 - Create Account with Background Profile (Priority: P3)

Student creates an account through BetterAuth, providing their background information (software and hardware experience). This profile is used for personalized content delivery and progress tracking.

**Why this priority**: User profiles enable personalized learning experiences and progress tracking.

**Independent Test**: Student can complete signup with required background information, receive authentication, and use the profile for personalization.

**Acceptance Scenarios**:

1. **Given** student wants to create an account, **When** student completes signup with name, email, role, software background, and hardware background, **Then** account is created and JWT is issued
2. **Given** student has an account, **When** student signs in, **Then** JWT is validated and used for personalization endpoints

---

### User Story 5 - Personalize Chapter Content (Priority: P3)

Student clicks the Personalize button at the start of a chapter to adapt content based on their stored profile. Content variants include beginner, intermediate, and advanced levels.

**Why this priority**: Personalization improves learning outcomes by matching content difficulty to student skill level.

**Independent Test**: Student can click Personalize, select a skill level, and see adapted content. Progress is tracked in the database.

**Acceptance Scenarios**:

1. **Given** student is viewing a chapter, **When** student clicks the Personalize button, **Then** content adapts to beginner, intermediate, or advanced variant based on selection
2. **Given** student uses personalization, **When** the content adapts, **Then** progress is recorded in the database

---

### User Story 6 - Translate Content to Urdu (Priority: P4)

Student clicks the Translate to Urdu button to view chapter content in Urdu. The translation preserves markdown formatting including code blocks and headings.

**Why this priority**: Urdu translation expands accessibility to Urdu-speaking students and supports internationalization goals.

**Independent Test**: Student can click translation button and receive properly formatted Urdu content.

**Acceptance Scenarios**:

1. **Given** student is viewing a chapter in English, **When** student clicks Translate to Urdu button, **Then** content is translated to readable Urdu
2. **Given** student views translated content, **When** reviewing code blocks and headings, **Then** formatting is preserved correctly

---

### Edge Cases

- What happens when the ChatBot cannot find relevant information in the selected text? (Fallback to context mode with user notification)
- How does the system handle invalid or expired JWT tokens? (Redirect to signin with appropriate error message)
- What occurs when translation service is unavailable? (Display error message and keep original content)
- How does the system behave when personalization profile is incomplete? (Use default intermediate level)
- What happens when module cards data fails to load? (Display fallback static cards)

## Requirements *(mandatory)*

### Functional Requirements

**Frontend UI**
- **FR-001**: Landing page MUST display a hero section matching the reference site design
- **FR-002**: Module cards MUST display title, week, icon, and animated hover effects
- **FR-003**: Chapter pages MUST include Personalize, TranslateUrdu, and ChatBot widget components
- **FR-004**: ChatBot widget MUST float at the bottom-right corner of chapter pages
- **FR-005**: ChatBot MUST support both selection mode and context mode
- **FR-006**: All pages MUST be responsive and mobile-friendly
- **FR-007**: Colors, fonts, favicon, logo, and icons MUST be consistent across the site

**Docusaurus Book**
- **FR-008**: All modules (ROS2, Gazebo/Unity, Isaac, VLA) MUST have chapters matching the weekly breakdown
- **FR-009**: Each chapter MUST contain learning objectives, theory, lab tasks, code examples, quizzes, and resources
- **FR-010**: MDX components (Personalize, TranslateUrdu, ChatSelection) MUST be implemented and functional
- **FR-011**: Deployment URL (GitHub Pages or Vercel) MUST be valid and publicly accessible

**RAG Chatbot**
- **FR-012**: Selected-text mode MUST return answers constrained to the selected text only
- **FR-013**: Context mode MUST return answers using top-5 retrieved chunks with source citations
- **FR-014**: Query latency MUST be under 2 seconds for local development
- **FR-015**: Retrieval latency MUST be under 500ms in cloud deployment

**BetterAuth Integration**
- **FR-016**: Signup MUST collect name, email, role, software background, and hardware background
- **FR-017**: JWT MUST be issued upon successful authentication
- **FR-018**: JWT MUST be validated for all personalization endpoint requests

**Personalization Engine**
- **FR-019**: Personalize button MUST be available at chapter start
- **FR-020**: Content variants MUST include beginner, intermediate, and advanced levels
- **FR-021**: Progress tracking MUST be recorded in the database

**Urdu Translation**
- **FR-022**: Translate button MUST return Urdu markdown content
- **FR-023**: Translation MUST preserve code blocks and headings formatting

### Key Entities

- **User**: Student, author, or admin with authentication credentials, background information (software/hardware experience), and role-based permissions
- **Chapter**: Educational content organized by modules and weeks, containing learning objectives, theory, lab tasks, code examples, and quizzes
- **Module**: Collection of related chapters (ROS2, Gazebo/Unity, Isaac, VLA, Capstone)
- **Personalization Profile**: User's skill level preferences and background information for content adaptation
- **Vector Chunk**: Text segments with metadata (doc_id, chapter, heading, chunk_index) stored in vector database
- **Translation Cache**: Cached Urdu translations of chapter content to reduce repeated LLM calls

## Assumptions

- Reference site (ai-native-book-iota.vercel.app) provides the UI design target
- BetterAuth handles OAuth flows and session management
- Qdrant Cloud Free Tier provides sufficient capacity for the textbook content
- LLM providers (Claude/OpenAI) are available for personalization and translation
- Students have modern browsers that support CSS animations and responsive design

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Landing page hero section renders correctly matching reference site design
- **SC-002**: Module cards display with animated hover effects on all screen sizes
- **SC-003**: All modules (ROS2, Gazebo/Unity, Isaac, VLA) have chapters matching weekly breakdown (100% coverage)
- **SC-004**: Each chapter contains all required elements (objectives, theory, labs, code, quizzes, resources)
- **SC-005**: ChatBot responds to selection mode queries with answers constrained to selected text
- **SC-006**: ChatBot context mode returns top-5 relevant chunks with source citations
- **SC-007**: Query latency meets targets (under 2s local, under 500ms cloud retrieval) for 95% of requests
- **SC-008**: Signup collects all required background information without errors
- **SC-009**: Personalization successfully adapts content to beginner, intermediate, and advanced levels
- **SC-010**: Urdu translation preserves code blocks and headings formatting
- **SC-011**: Deployment URL is publicly accessible and all pages load correctly
- **SC-012**: UI is consistent across site (colors, fonts, favicon, logo, icons)

## Clarifications

### Session 2025-12-06

- Q: Include Jetson / Unitree SDK code in repo or via external links? → A: Include Jetson/Unitree SDK code in the repository
- Q: Fully generated Urdu translations for all chapters before submission or on-demand? → A: Generate translations on-demand when users request them
- Q: Authentication approach - OAuth with JWT tokens vs alternatives? → A: OAuth with JWT tokens via BetterAuth
- Q: Embeddings and LLM provider selection? → A: OpenAI embeddings with fallback to Claude
- Q: Deployment and hosting architecture? → A: GitHub Pages for frontend, cloud backend
