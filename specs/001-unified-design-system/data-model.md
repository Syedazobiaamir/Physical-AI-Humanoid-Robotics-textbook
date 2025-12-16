# Data Model: AI-Native Technical Textbook Platform

**Feature**: 001-unified-design-system
**Date**: 2025-12-15 (Updated)
**Status**: Complete

## Overview

This document defines the data entities, relationships, and validation rules for the AI-Native Technical Textbook Platform with Clerk authentication and Dark Blue + Yellow theme.

---

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│      User       │───────│   UserProfile   │
│  (Clerk-based)  │  1:1  │  (Background)   │
└─────────────────┘       └─────────────────┘
         │                        │
         │ 1:N                    │
         ▼                        │
┌─────────────────┐               │
│   ChatSession   │───────────────┘
└─────────────────┘  (personalization context)
         │
         │ 1:N
         ▼
┌─────────────────┐
│   ChatMessage   │
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│ PlatformStats   │       │TranslationCache │
│   (Singleton)   │       │    (Chapter)    │
└─────────────────┘       └─────────────────┘
```

---

## Entities

### 1. User

**Description**: User account linked to Clerk authentication.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | VARCHAR(255) | PK, NOT NULL | Clerk user_id |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email from Clerk |
| name | VARCHAR(255) | NULL | Display name from Clerk |
| avatar_url | VARCHAR(500) | NULL | Profile image URL |
| role | VARCHAR(50) | NOT NULL, DEFAULT 'student' | student, instructor |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Validation Rules**:
- id is provided by Clerk (not auto-generated)
- email must be valid format (RFC 5322)

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (email)

---

### 2. UserProfile (Personalization Preferences)

**Description**: Extended user profile with learning background for personalization.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Auto-generated UUID |
| user_id | VARCHAR(255) | FK → User.id, UNIQUE, NOT NULL | Clerk user reference |
| software_level | ENUM | NOT NULL, DEFAULT 'beginner' | beginner, intermediate, advanced |
| hardware_exposure | ENUM | NOT NULL, DEFAULT 'none' | none, some, extensive |
| robotics_experience | ENUM | NOT NULL, DEFAULT 'none' | none, some, extensive |
| language_preference | ENUM | NOT NULL, DEFAULT 'en' | en (English), ur (Urdu) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Profile creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Validation Rules**:
- software_level MUST be one of: 'beginner', 'intermediate', 'advanced'
- hardware_exposure MUST be one of: 'none', 'some', 'extensive'
- robotics_experience MUST be one of: 'none', 'some', 'extensive'
- language_preference MUST be one of: 'en', 'ur'

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (user_id)

---

### 3. Chapter

**Description**: Course chapter content metadata (MDX files in Docusaurus).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | VARCHAR(255) | PK, NOT NULL | Chapter identifier (slug) |
| title | VARCHAR(255) | NOT NULL | Chapter title |
| module | VARCHAR(50) | NOT NULL | Module name (module-1, module-2, etc.) |
| week | INTEGER | NOT NULL | Week number (1-16) |
| content_path | VARCHAR(500) | NOT NULL | Path to MDX file |
| learning_objectives | TEXT[] | NOT NULL | Array of learning objectives |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Validation Rules**:
- id must be lowercase alphanumeric with hyphens
- week MUST be between 1 and 16
- content_path MUST be valid file path

**Indexes**:
- PRIMARY KEY (id)
- INDEX (module)
- INDEX (week)

---

### 4. ChatSession

**Description**: A conversation session for RAG chatbot.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | VARCHAR(255) | FK → User.id, NULL | Associated user (NULL for anonymous) |
| chapter_id | VARCHAR(255) | FK → Chapter.id, NULL | Chapter context (if any) |
| is_active | BOOLEAN | NOT NULL, DEFAULT true | Session active status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session start time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last activity time |

**Validation Rules**:
- Session auto-closes after 30 minutes of inactivity

**Indexes**:
- PRIMARY KEY (id)
- INDEX (user_id)
- INDEX (chapter_id)
- INDEX (is_active, updated_at)

---

### 5. ChatMessage

**Description**: Individual message in a chat session.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| session_id | UUID | FK → ChatSession.id, NOT NULL | Parent session |
| role | ENUM | NOT NULL | 'user' or 'assistant' |
| content | TEXT | NOT NULL | Message content |
| selected_context | TEXT | NULL | User-selected text (Context Selection Skill) |
| skill_used | VARCHAR(100) | NULL | Which skill generated this (assistant only) |
| tokens_used | INTEGER | NULL | Token count for assistant messages |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

**Validation Rules**:
- role MUST be one of: 'user', 'assistant'
- content MUST NOT be empty
- selected_context only populated for user messages with text selection
- skill_used only populated for assistant messages

**Indexes**:
- PRIMARY KEY (id)
- INDEX (session_id, created_at)

---

### 6. TranslationCache

**Description**: Cached Urdu translations for chapters.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| chapter_id | VARCHAR(255) | FK → Chapter.id, NOT NULL | Source chapter |
| content_hash | VARCHAR(64) | NOT NULL | SHA-256 of original content |
| urdu_content | TEXT | NOT NULL | Translated content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Translation time |
| expires_at | TIMESTAMP | NOT NULL | Cache expiration (30 days) |

**Validation Rules**:
- content_hash must be 64-char hex string (SHA-256)
- expires_at MUST be > created_at
- UNIQUE constraint on (chapter_id, content_hash)

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (chapter_id, content_hash)
- INDEX (expires_at)

---

### 7. PlatformStats

**Description**: Platform-wide statistics for landing page.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, DEFAULT 1 | Singleton row |
| books_count | INTEGER | NOT NULL, DEFAULT 1 | Number of books/courses |
| active_users | INTEGER | NOT NULL, DEFAULT 0 | Active user count |
| ai_interactions | INTEGER | NOT NULL, DEFAULT 0 | Total AI skill invocations |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last stats update |

**Validation Rules**:
- Only one row exists (id = 1)
- All counts >= 0

**Indexes**:
- PRIMARY KEY (id)

---

## Design Tokens Entity (Frontend Only)

**Description**: CSS custom properties for Dark Blue + Yellow theme. Not stored in database.

```typescript
interface DesignTokens {
  colors: {
    primaryDark: '#1a1a2e';      // Dark Blue - backgrounds
    primaryAccent: '#ffd700';    // Yellow - accents, CTAs
    background: '#0f0f1a';       // Darker background variant
    surface: '#252540';          // Card backgrounds
    textPrimary: '#ffffff';      // Primary text
    textSecondary: '#b0b0c0';    // Muted text
    hover: '#ffd700';            // Yellow hover
    focusRing: 'rgba(255, 215, 0, 0.3)'; // Yellow focus
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
    '2xl': '48px';
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
    ├── User closes chat → Closed (is_active=false)
    │
    └── Inactivity timeout (30min) → Closed (is_active=false)
```

### UserProfile Completion States

```
Created (after Clerk signup)
    │
    └── User completes background questions → Complete
        │
        └── User updates preferences → Updated (updated_at refreshed)
```

---

## Qdrant Vector Schema

**Collection**: `textbook_content`

| Field | Type | Description |
|-------|------|-------------|
| id | string | UUID of the chunk |
| vector | float[768] | text-embedding-004 embedding |
| payload.chapter_id | string | Chapter identifier |
| payload.module | string | Module name |
| payload.section_title | string | Section within chapter |
| payload.content | string | Original text chunk (~500 tokens) |
| payload.token_count | int | Chunk token count |

**Index Configuration**:
- Distance metric: Cosine
- Vector size: 768 (text-embedding-004)
- HNSW index for fast ANN search

---

## SQL Schema (Neon Postgres)

```sql
-- Enums
CREATE TYPE software_level AS ENUM ('beginner', 'intermediate', 'advanced');
CREATE TYPE experience_level AS ENUM ('none', 'some', 'extensive');
CREATE TYPE language_preference AS ENUM ('en', 'ur');
CREATE TYPE message_role AS ENUM ('user', 'assistant');

-- Users (Clerk-linked)
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,          -- Clerk user_id
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url VARCHAR(500),
    role VARCHAR(50) NOT NULL DEFAULT 'student',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- User Profiles (Personalization)
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    software_level software_level NOT NULL DEFAULT 'beginner',
    hardware_exposure experience_level NOT NULL DEFAULT 'none',
    robotics_experience experience_level NOT NULL DEFAULT 'none',
    language_preference language_preference NOT NULL DEFAULT 'en',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Chapters
CREATE TABLE chapters (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    module VARCHAR(50) NOT NULL,
    week INTEGER NOT NULL CHECK (week BETWEEN 1 AND 16),
    content_path VARCHAR(500) NOT NULL,
    learning_objectives TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Chat Sessions
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE SET NULL,
    chapter_id VARCHAR(255) REFERENCES chapters(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Chat Messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role message_role NOT NULL,
    content TEXT NOT NULL CHECK (content <> ''),
    selected_context TEXT,
    skill_used VARCHAR(100),
    tokens_used INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Translation Cache
CREATE TABLE translation_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id VARCHAR(255) NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    content_hash VARCHAR(64) NOT NULL,
    urdu_content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    UNIQUE (chapter_id, content_hash)
);

-- Platform Statistics (Singleton)
CREATE TABLE platform_stats (
    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    books_count INTEGER NOT NULL DEFAULT 1,
    active_users INTEGER NOT NULL DEFAULT 0,
    ai_interactions INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Insert singleton row
INSERT INTO platform_stats (id) VALUES (1) ON CONFLICT DO NOTHING;

-- Indexes
CREATE INDEX idx_user_profiles_user ON user_profiles(user_id);
CREATE INDEX idx_chapters_module ON chapters(module);
CREATE INDEX idx_chapters_week ON chapters(week);
CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_chapter ON chat_sessions(chapter_id);
CREATE INDEX idx_chat_sessions_active ON chat_sessions(is_active, updated_at);
CREATE INDEX idx_chat_messages_session_time ON chat_messages(session_id, created_at);
CREATE INDEX idx_translation_cache_chapter ON translation_cache(chapter_id);
CREATE INDEX idx_translation_cache_expiry ON translation_cache(expires_at);
```

---

## Summary

7 entities defined with clear relationships:
- **User** ↔ **UserProfile** (1:1) - Clerk-linked with personalization prefs
- **User** → **ChatSession** (1:N)
- **Chapter** → **ChatSession** (1:N)
- **ChatSession** → **ChatMessage** (1:N)
- **Chapter** → **TranslationCache** (1:N)
- **PlatformStats** (Singleton for landing page)

Plus Qdrant vector schema for RAG and frontend DesignTokens interface for Dark Blue + Yellow theme.
