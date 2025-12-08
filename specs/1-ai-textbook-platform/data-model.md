# Data Model: Physical AI & Humanoid Robotics Textbook Platform

**Date**: 2025-12-06
**Updated**: 2025-12-07
**Version**: 2.0.0
**Feature**: 1-ai-textbook-platform
**Plan**: [Implementation Plan](plan.md)

## Overview

This document defines the data models for the Physical AI & Humanoid Robotics textbook platform, including entities, relationships, and validation rules based on the feature specification.

## v2.0.0 Additions

### 8. Module
**Description**: Collection of related chapters representing a major topic area
**Fields**:
- `id` (string, required): Unique identifier (e.g., 'module-1', 'module-2')
- `title` (string, required): Module title (e.g., 'ROS2 Fundamentals')
- `description` (string, required): Brief description for module card
- `icon` (string, required): Icon name or path for display
- `weeks` (string, required): Week range (e.g., 'Weeks 1-3')
- `order` (integer, required): Display order on landing page
- `color` (string, optional): Accent color for module card

**Validation Rules**:
- Title and description are required
- Order must be unique and non-negative
- Icon must reference valid icon asset

## Core Entities

### 1. User
**Description**: Represents platform users including students, authors, and admins
**Fields**:
- `id` (string, required): Unique identifier (UUID)
- `name` (string, required): Full name of the user
- `email` (string, required): Email address (unique, valid email format)
- `role` (string, required): User role ('student', 'author', 'admin')
- `software_background` (string, required): Software experience level
- `hardware_background` (string, required): Hardware experience level
- `created_at` (datetime, required): Account creation timestamp
- `updated_at` (datetime, required): Last update timestamp
- `preferences` (object, optional): Personalization preferences

**Validation Rules**:
- Email must be unique and valid format
- Role must be one of predefined values
- Name and email are required
- Background fields must be from predefined options

### 2. Chapter
**Description**: Educational content organized by modules and weeks
**Fields**:
- `id` (string, required): Unique identifier (UUID)
- `title` (string, required): Chapter title
- `module` (string, required): Module identifier ('Module 1', 'Module 2', etc.)
- `week` (integer, required): Week number (1-13)
- `learning_objectives` (array, required): Array of learning objectives
- `content` (string, required): Chapter content in MDX format
- `code_examples` (array, optional): Array of code examples
- `lab_tasks` (array, optional): Array of lab task descriptions
- `resources` (array, optional): Array of additional resources
- `created_at` (datetime, required): Creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Validation Rules**:
- Title and content are required
- Module must be valid (Module 1-4)
- Week must be between 1-13
- Learning objectives must be a non-empty array

### 3. Quiz
**Description**: Set of questions for chapter assessment
**Fields**:
- `id` (string, required): Unique identifier (UUID)
- `chapter_id` (string, required): Reference to associated chapter
- `questions` (array, required): Array of question objects
- `created_at` (datetime, required): Creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Question Object**:
- `id` (string, required): Question identifier
- `text` (string, required): Question text
- `options` (array, required): Array of 4 answer options
- `correct_answer` (string, required): Index or text of correct answer
- `explanation` (string, optional): Explanation of correct answer

**Validation Rules**:
- Chapter ID must reference existing chapter
- Questions array must contain exactly 5 questions
- Each question must have 4 options
- Correct answer must match one of the options

### 4. PersonalizationProfile
**Description**: User's skill level preferences for content adaptation
**Fields**:
- `id` (string, required): Unique identifier (UUID)
- `user_id` (string, required): Reference to user
- `chapter_id` (string, required): Reference to chapter
- `skill_level` (string, required): Preferred skill level ('beginner', 'intermediate', 'advanced')
- `created_at` (datetime, required): Creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Validation Rules**:
- User ID must reference existing user
- Chapter ID must reference existing chapter
- Skill level must be one of predefined values

### 5. ProgressTracking
**Description**: Tracks user progress through chapters and quizzes
**Fields**:
- `id` (string, required): Unique identifier (UUID)
- `user_id` (string, required): Reference to user
- `chapter_id` (string, required): Reference to chapter
- `quiz_score` (number, optional): Score on chapter quiz (0-100)
- `completed_at` (datetime, optional): Completion timestamp
- `created_at` (datetime, required): Creation timestamp
- `updated_at` (datetime, required): Last update timestamp

**Validation Rules**:
- User ID must reference existing user
- Chapter ID must reference existing chapter
- Quiz score must be between 0-100 if provided

### 6. VectorChunk
**Description**: Text segments with metadata stored in vector database
**Fields**:
- `id` (string, required): Unique identifier (UUID)
- `doc_id` (string, required): Document identifier
- `chapter_id` (string, required): Reference to chapter
- `heading` (string, optional): Section heading
- `chunk_index` (integer, required): Order within document
- `content` (string, required): Chunk text content
- `embedding` (array, required): Vector embedding array
- `created_at` (datetime, required): Creation timestamp

**Validation Rules**:
- Content must be non-empty
- Embedding must be a valid vector array
- Chunk index must be non-negative

### 7. TranslationCache
**Description**: Caches Urdu translations to improve performance
**Fields**:
- `id` (string, required): Unique identifier (UUID)
- `chapter_id` (string, required): Reference to chapter
- `content_hash` (string, required): Hash of original content
- `urdu_content` (string, required): Translated content
- `created_at` (datetime, required): Creation timestamp
- `expires_at` (datetime, required): Expiration timestamp

**Validation Rules**:
- Chapter ID must reference existing chapter
- Content hash and Urdu content must be non-empty
- Expires at must be in the future

## Relationships

```
User 1---* PersonalizationProfile
User 1---* ProgressTracking
User 1---* TranslationCache (via session context)

Chapter 1---* Quiz
Chapter 1---* PersonalizationProfile
Chapter 1---* ProgressTracking
Chapter 1---* VectorChunk
Chapter 1---* TranslationCache

Quiz 1---* Question (embedded in questions array)
```

## State Transitions

### User Role Transitions
- `student` → `author` (admin action)
- `student` → `admin` (admin action)
- `author` → `admin` (admin action)

### Progress Tracking States
- `not_started` → `in_progress` (when user begins chapter)
- `in_progress` → `completed` (when user finishes chapter)
- `completed` → `reviewed` (when user completes quiz)

## Indexes

### Primary Indexes
- User: `email` (unique)
- Chapter: `module`, `week` (composite)
- Quiz: `chapter_id` (foreign key)

### Secondary Indexes
- PersonalizationProfile: `user_id`, `chapter_id` (composite)
- ProgressTracking: `user_id`, `chapter_id` (composite)
- VectorChunk: `chapter_id`, `chunk_index` (composite)
- TranslationCache: `chapter_id`, `content_hash` (composite)

## Constraints

### Referential Integrity
- All foreign key relationships must reference existing records
- Deletion of parent records should cascade appropriately (e.g., deleting a chapter deletes related quizzes)

### Data Quality
- All timestamps must be in ISO 8601 format
- All text fields must be properly sanitized to prevent XSS
- Email validation follows RFC 5322 standards