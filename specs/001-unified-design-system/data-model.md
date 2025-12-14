# Data Model: Unified UI/UX + Chatbot Design System

**Feature**: 001-unified-design-system
**Date**: 2025-12-13
**Status**: Complete

## Overview

This document defines the data entities, relationships, and validation rules for the Unified Design System feature.

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────────┐       ┌──────────────┐
│    User     │───────│  UserProfile    │       │   Chapter    │
└─────────────┘  1:1  └─────────────────┘       └──────────────┘
       │                                               │
       │ 1:N                                          │
       ▼                                              │
┌─────────────────┐                                   │
│  ChatSession    │───────────────────────────────────┘
└─────────────────┘  N:1 (chapter context)
       │
       │ 1:N
       ▼
┌─────────────────┐
│  ChatMessage    │
└─────────────────┘
```

---

## Entities

### 1. User

**Description**: Core user account managed by Better-Auth.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| email_verified | BOOLEAN | DEFAULT false | Email verification status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Password minimum 8 characters, at least one number and one letter

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (email)

---

### 2. UserProfile

**Description**: Extended user profile with learning preferences.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | UUID | FK → User.id, UNIQUE, NOT NULL | Associated user |
| display_name | VARCHAR(100) | NULL | Optional display name |
| software_background | TEXT | NULL | User's software experience description |
| hardware_background | TEXT | NULL | User's hardware experience description |
| skill_level | ENUM | NOT NULL, DEFAULT 'beginner' | beginner, intermediate, advanced |
| language_preference | ENUM | NOT NULL, DEFAULT 'en' | en (English), ur (Urdu) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Profile creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Validation Rules**:
- skill_level MUST be one of: 'beginner', 'intermediate', 'advanced'
- language_preference MUST be one of: 'en', 'ur'
- display_name max 100 characters

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (user_id)

---

### 3. Chapter

**Description**: Course chapter content metadata.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-friendly identifier |
| title | VARCHAR(255) | NOT NULL | Chapter title |
| module_number | INTEGER | NOT NULL | Module (1-4, 5=Capstone) |
| chapter_number | INTEGER | NOT NULL | Chapter within module |
| content_path | VARCHAR(500) | NOT NULL | Path to MDX file |
| embedding_collection | VARCHAR(100) | NOT NULL | Qdrant collection name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Validation Rules**:
- slug must be lowercase alphanumeric with hyphens only
- module_number MUST be 1-5
- content_path MUST be valid file path

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (slug)
- INDEX (module_number, chapter_number)

---

### 4. ChatSession

**Description**: A conversation session between user and chatbot.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | UUID | FK → User.id, NULL | Associated user (NULL for anonymous) |
| chapter_id | UUID | FK → Chapter.id, NULL | Chapter context (if any) |
| session_token | VARCHAR(64) | UNIQUE, NOT NULL | Anonymous session identifier |
| is_active | BOOLEAN | NOT NULL, DEFAULT true | Session active status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session start time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last activity time |
| closed_at | TIMESTAMP | NULL | Session end time |

**Validation Rules**:
- session_token must be cryptographically random 64-char hex string
- Either user_id OR session_token must identify the session

**Indexes**:
- PRIMARY KEY (id)
- INDEX (user_id)
- INDEX (chapter_id)
- UNIQUE INDEX (session_token)

---

### 5. ChatMessage

**Description**: Individual message in a chat session.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| session_id | UUID | FK → ChatSession.id, NOT NULL | Parent session |
| role | ENUM | NOT NULL | 'user' or 'assistant' |
| content | TEXT | NOT NULL | Message content |
| selected_context | TEXT | NULL | User-selected text context |
| tokens_used | INTEGER | NULL | Token count for assistant messages |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

**Validation Rules**:
- role MUST be one of: 'user', 'assistant'
- content MUST NOT be empty
- selected_context only populated for user messages with text selection

**Indexes**:
- PRIMARY KEY (id)
- INDEX (session_id, created_at)

---

### 6. PersonalizedContent (Cache)

**Description**: Cached personalized chapter content for users.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | UUID | FK → User.id, NOT NULL | Target user |
| chapter_id | UUID | FK → Chapter.id, NOT NULL | Source chapter |
| personalization_type | ENUM | NOT NULL | 'beginner', 'hardware', 'urdu' |
| content | TEXT | NOT NULL | Transformed content |
| agent_used | VARCHAR(100) | NOT NULL | Agent that generated content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Generation time |
| expires_at | TIMESTAMP | NOT NULL | Cache expiration |

**Validation Rules**:
- personalization_type MUST be one of: 'beginner', 'hardware', 'urdu'
- expires_at MUST be > created_at
- UNIQUE constraint on (user_id, chapter_id, personalization_type)

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (user_id, chapter_id, personalization_type)
- INDEX (expires_at)

---

## Design Tokens Entity (Frontend Only)

**Description**: CSS custom properties for design system consistency. Not stored in database.

```typescript
interface DesignTokens {
  colors: {
    deepSpaceBlue: '#0B1020';
    neuralIndigo: '#1E2A78';
    electricCyan: '#00E5FF';
    softAiViolet: '#7C7CFF';
    textPrimary: '#EAEAF0';
    textMuted: '#9AA4BF';
    cardBackground: '#121830';
    divider: '#1F2A44';
  };
  typography: {
    fontHeading: 'Space Grotesk';
    fontBody: 'Inter';
    fontCode: 'JetBrains Mono';
    sizeH1: '48px';
    sizeH2: '36px';
    sizeH3: '28px';
    sizeBody: '16px';
  };
  spacing: {
    xs: '4px';
    sm: '8px';
    md: '16px';
    lg: '24px';
    xl: '32px';
  };
  animation: {
    hoverLift: '-8px';
    transitionDuration: '200ms';
    springStiffness: 300;
  };
}
```

---

## State Transitions

### ChatSession Lifecycle

```
Created (is_active=true)
    │
    ├── User sends message → Updated (updated_at refreshed)
    │
    ├── User closes chat → Closed (is_active=false, closed_at set)
    │
    └── Inactivity timeout (30min) → Closed (is_active=false, closed_at set)
```

### UserProfile Completion States

```
Incomplete (after signup, before profile setup)
    │
    └── User completes profile form → Complete
        │
        └── User updates preferences → Updated (updated_at refreshed)
```

---

## Qdrant Vector Schema

**Collection**: `course_content`

| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID of the chunk |
| vector | float[768] | text-embedding-004 embedding |
| payload.chapter_id | string | Chapter UUID |
| payload.chapter_slug | string | Chapter slug for reference |
| payload.section_title | string | Section within chapter |
| payload.content | string | Original text chunk |
| payload.token_count | int | Chunk token count |

**Index Configuration**:
- Distance metric: Cosine
- Vector size: 768 (text-embedding-004)
- HNSW index for fast ANN search

---

## SQL Schema (Neon Postgres)

```sql
-- Enums
CREATE TYPE skill_level AS ENUM ('beginner', 'intermediate', 'advanced');
CREATE TYPE language_preference AS ENUM ('en', 'ur');
CREATE TYPE message_role AS ENUM ('user', 'assistant');
CREATE TYPE personalization_type AS ENUM ('beginner', 'hardware', 'urdu');

-- Users (Better-Auth managed)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- User Profiles
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    display_name VARCHAR(100),
    software_background TEXT,
    hardware_background TEXT,
    skill_level skill_level NOT NULL DEFAULT 'beginner',
    language_preference language_preference NOT NULL DEFAULT 'en',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Chapters
CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    module_number INTEGER NOT NULL CHECK (module_number BETWEEN 1 AND 5),
    chapter_number INTEGER NOT NULL,
    content_path VARCHAR(500) NOT NULL,
    embedding_collection VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Chat Sessions
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    chapter_id UUID REFERENCES chapters(id) ON DELETE SET NULL,
    session_token VARCHAR(64) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMP
);

-- Chat Messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role message_role NOT NULL,
    content TEXT NOT NULL CHECK (content <> ''),
    selected_context TEXT,
    tokens_used INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Personalized Content Cache
CREATE TABLE personalized_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    personalization_type personalization_type NOT NULL,
    content TEXT NOT NULL,
    agent_used VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    UNIQUE (user_id, chapter_id, personalization_type)
);

-- Indexes
CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_chapter ON chat_sessions(chapter_id);
CREATE INDEX idx_chat_messages_session_time ON chat_messages(session_id, created_at);
CREATE INDEX idx_personalized_content_expiry ON personalized_content(expires_at);
CREATE INDEX idx_chapters_module ON chapters(module_number, chapter_number);
```

---

## Summary

6 entities defined with clear relationships:
- **User** ↔ **UserProfile** (1:1)
- **User** → **ChatSession** (1:N)
- **Chapter** → **ChatSession** (1:N)
- **ChatSession** → **ChatMessage** (1:N)
- **User** + **Chapter** → **PersonalizedContent** (N:M with caching)

Plus Qdrant vector schema for RAG and frontend DesignTokens interface.
