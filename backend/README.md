---
title: Physical AI Textbook API
emoji: 🤖
colorFrom: blue
colorTo: yellow
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Physical AI & Humanoid Robotics Textbook API

Backend API for the AI-native textbook platform providing:
- RAG-based chat functionality
- User authentication via Clerk
- Content personalization
- Urdu translation
- Progress tracking
- Quiz generation

## API Documentation

Once deployed, access the interactive API docs at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health` | Health check |
| `/api/v1/rag/chat` | RAG-based chat |
| `/api/v1/auth/*` | Authentication |
| `/api/v1/personalization/*` | Content personalization |
| `/api/v1/translation/*` | Urdu translation |
| `/api/v1/progress/*` | Progress tracking |

## Environment Variables

Configure these in your Hugging Face Space settings:
- `GEMINI_API_KEY` - Google Gemini API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `NEON_DB_URL` - PostgreSQL connection string
- `CLERK_SECRET_KEY` - Clerk authentication secret
- `JWT_SECRET_KEY` - JWT signing key
