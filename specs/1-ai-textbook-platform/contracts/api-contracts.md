# API Contracts: Physical AI & Humanoid Robotics Textbook Platform

**Date**: 2025-12-06
**Updated**: 2025-12-07
**Version**: 2.0.0
**Feature**: 1-ai-textbook-platform
**Plan**: [Implementation Plan](../plan.md)

## Overview

This document defines the API contracts for the Physical AI & Humanoid Robotics textbook platform, specifying endpoints, request/response formats, and integration patterns based on the functional requirements.

## v2.0.0 Additions

### Modules Endpoint

#### GET /api/v1/modules
Get all modules for landing page display

**Response**:
- 200:
```json
{
  "modules": [
    {
      "id": "module-1",
      "title": "ROS2 Fundamentals",
      "description": "Introduction to Robot Operating System 2",
      "icon": "robot",
      "weeks": "Weeks 1-3",
      "order": 1,
      "color": "#3B82F6"
    }
  ]
}
```

## Authentication

### OAuth with JWT
**Base URL**: `/api/v1/auth`

#### POST /login/oauth
Initiate OAuth login flow with supported providers

**Request**:
```json
{
  "provider": "google|github",
  "redirect_uri": "string"
}
```

**Response**:
- 200: `{ "auth_url": "string" }`
- 400: `{ "error": "invalid_provider" }`

#### POST /login/callback
Handle OAuth callback and return JWT

**Request**:
```json
{
  "code": "string",
  "provider": "google|github"
}
```

**Response**:
- 200: `{ "access_token": "string", "refresh_token": "string", "user": { ... } }`
- 400: `{ "error": "invalid_code" }`
- 401: `{ "error": "authentication_failed" }`

#### POST /refresh
Refresh access token

**Request**:
```json
{
  "refresh_token": "string"
}
```

**Response**:
- 200: `{ "access_token": "string" }`
- 401: `{ "error": "invalid_token" }`

## RAG Chatbot

### Base URL: `/api/v1/rag`

#### POST /query
Query the RAG system for answers

**Headers**:
- `Authorization: Bearer {token}` (optional for basic queries)

**Request**:
```json
{
  "query": "string",
  "context_mode": "selection|general",
  "selected_text": "string", // required if context_mode is "selection"
  "chapter_id": "string" // optional, for context
}
```

**Response**:
- 200: `{ "answer": "string", "sources": ["string"], "latency": "number" }`
- 400: `{ "error": "invalid_request" }`
- 429: `{ "error": "rate_limited" }`

#### GET /health
Check RAG system health

**Response**:
- 200: `{ "status": "healthy", "models": ["openai", "anthropic"] }`

## Personalization

### Base URL: `/api/v1/personalization`

#### GET /preferences/{chapter_id}
Get user's personalization preferences for a chapter

**Headers**:
- `Authorization: Bearer {token}`

**Response**:
- 200: `{ "skill_level": "beginner|intermediate|advanced", "customizations": {} }`
- 401: `{ "error": "unauthorized" }`
- 404: `{ "error": "preferences_not_found" }`

#### PUT /preferences/{chapter_id}
Set user's personalization preferences for a chapter

**Headers**:
- `Authorization: Bearer {token}`

**Request**:
```json
{
  "skill_level": "beginner|intermediate|advanced",
  "customizations": {}
}
```

**Response**:
- 200: `{ "success": true }`
- 400: `{ "error": "invalid_preferences" }`
- 401: `{ "error": "unauthorized" }`

#### POST /adapt-content
Get personalized content adaptation

**Headers**:
- `Authorization: Bearer {token}`

**Request**:
```json
{
  "chapter_id": "string",
  "skill_level": "beginner|intermediate|advanced",
  "content_format": "mdx|html"
}
```

**Response**:
- 200: `{ "adapted_content": "string" }`
- 400: `{ "error": "invalid_request" }`
- 401: `{ "error": "unauthorized" }`

## Urdu Translation

### Base URL: `/api/v1/translation`

#### POST /urdu
Translate content to Urdu

**Headers**:
- `Authorization: Bearer {token}` (optional)

**Request**:
```json
{
  "content": "string",
  "content_type": "chapter|section|text",
  "preserve_formatting": true
}
```

**Response**:
- 200: `{ "urdu_content": "string", "cache_hit": true|false }`
- 400: `{ "error": "invalid_content" }`
- 429: `{ "error": "rate_limited" }`

#### GET /urdu/{chapter_id}
Get cached Urdu translation for a chapter

**Headers**:
- `Authorization: Bearer {token}` (optional)

**Response**:
- 200: `{ "urdu_content": "string", "last_updated": "datetime" }`
- 404: `{ "error": "translation_not_found" }`

## Quiz System

### Base URL: `/api/v1/quizzes`

#### GET /{chapter_id}
Get quiz for a specific chapter

**Headers**:
- `Authorization: Bearer {token}` (optional for retrieval)

**Response**:
- 200: `{ "quiz_id": "string", "questions": [...], "created_at": "datetime" }`
- 404: `{ "error": "quiz_not_found" }`

#### POST /{chapter_id}/submit
Submit quiz answers

**Headers**:
- `Authorization: Bearer {token}`

**Request**:
```json
{
  "answers": [
    {
      "question_id": "string",
      "selected_option": "string|number"
    }
  ]
}
```

**Response**:
- 200: `{ "score": "number", "results": [...], "feedback": "string" }`
- 400: `{ "error": "invalid_answers" }`
- 401: `{ "error": "unauthorized" }`

## Content Management

### Base URL: `/api/v1/content`

#### GET /chapters
List all chapters

**Query Parameters**:
- `module` (optional): Filter by module
- `week_from` (optional): Filter by week range
- `week_to` (optional): Filter by week range

**Response**:
- 200: `{ "chapters": [...], "total": "number" }`

#### GET /chapters/{chapter_id}
Get specific chapter content

**Response**:
- 200: `{ "chapter": { ... }, "next_chapter": "string", "prev_chapter": "string" }`
- 404: `{ "error": "chapter_not_found" }`

#### GET /chapters/{chapter_id}/sdk-content
Get associated SDK code examples

**Response**:
- 200: `{ "sdk_examples": [...], "repository_links": [...] }`
- 404: `{ "error": "sdk_content_not_found" }`

## Progress Tracking

### Base URL: `/api/v1/progress`

#### GET /user/{user_id}
Get user's progress summary

**Headers**:
- `Authorization: Bearer {token}` (user must be self or admin)

**Response**:
- 200: `{ "completed_chapters": ["string"], "quiz_scores": [...], "overall_progress": "number" }`

#### POST /track
Update progress for a chapter

**Headers**:
- `Authorization: Bearer {token}`

**Request**:
```json
{
  "chapter_id": "string",
  "action": "started|completed|quiz_completed",
  "metadata": {}
}
```

**Response**:
- 200: `{ "success": true, "progress_updated": "datetime" }`
- 400: `{ "error": "invalid_action" }`
- 401: `{ "error": "unauthorized" }`

## Error Handling

### Standard Error Format
```json
{
  "error": "error_code",
  "message": "human_readable_message",
  "details": {} // optional additional details
}
```

### Common Error Codes
- `unauthorized`: Authentication required or invalid
- `forbidden`: Insufficient permissions
- `not_found`: Requested resource does not exist
- `invalid_request`: Request validation failed
- `rate_limited`: API rate limit exceeded
- `service_unavailable`: Downstream service error
- `internal_error`: Unexpected server error

## Rate Limiting

All authenticated endpoints are rate-limited at 100 requests per hour per user.
All unauthenticated endpoints are rate-limited at 10 requests per hour per IP.

Rate limit headers:
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time when limit resets

## Versioning

All API endpoints use versioning in the URL path: `/api/v{version_number}/endpoint`.
Current version: v1