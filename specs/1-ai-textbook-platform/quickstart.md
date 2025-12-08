# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Platform

**Date**: 2025-12-06
**Updated**: 2025-12-07
**Version**: 2.0.0
**Feature**: 1-ai-textbook-platform
**Plan**: [Implementation Plan](plan.md)

## Overview

This guide provides a quick setup and run instructions for the Physical AI & Humanoid Robotics textbook platform. Follow these steps to get the development environment running.

## v2.0.0 Updates

- Added BetterAuth configuration for OAuth
- Added frontend component structure (Hero, ModuleCard, ChatBot, etc.)
- Updated Docusaurus configuration for custom theme
- Added animation and responsive design requirements

## Prerequisites

- Node.js 18+ (for Docusaurus frontend)
- Python 3.11+ (for FastAPI backend)
- Git
- Docker (optional, for containerized deployment)
- OpenAI API key
- Anthropic API key (for fallback)
- Qdrant Cloud account (free tier)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Frontend Setup (Docusaurus)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Update .env with your configuration
# (see Environment Variables section below)
```

### 3. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Update .env with your configuration
# (see Environment Variables section below)
```

### 4. Environment Variables

#### Frontend (.env)
```env
# Backend API URL
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1

# Authentication
REACT_APP_AUTH_PROVIDER=google  # or github
REACT_APP_CLIENT_ID=your_oauth_client_id
REACT_APP_CLIENT_SECRET=your_oauth_client_secret
```

#### Backend (.env)
```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Qdrant Configuration
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_CLOUD=true

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname
NEON_DB_URL=your_neon_database_url

# Authentication
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
PROJECT_NAME=Physical AI & Humanoid Robotics Textbook
API_V1_STR=/api/v1
DEBUG=true
```

## Running the Application

### 1. Start the Backend

```bash
# From backend directory
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend

```bash
# From frontend directory
npm start
```

### 3. Access the Application

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Backend redoc: http://localhost:8000/redoc

## Development Commands

### Frontend Commands
```bash
# Install dependencies
npm install

# Run in development mode
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

### Backend Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn src.main:app --reload

# Run tests
pytest

# Format code
black src/
flake8 src/

# Run with gunicorn (production)
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/oauth` - OAuth login
- `POST /api/v1/auth/login/callback` - OAuth callback
- `POST /api/v1/auth/refresh` - Token refresh

### RAG Chatbot
- `POST /api/v1/rag/query` - Query RAG system
- `GET /api/v1/rag/health` - Health check

### Personalization
- `GET /api/v1/personalization/preferences/{chapter_id}` - Get preferences
- `PUT /api/v1/personalization/preferences/{chapter_id}` - Set preferences
- `POST /api/v1/personalization/adapt-content` - Adapt content

### Translation
- `POST /api/v1/translation/urdu` - Translate to Urdu
- `GET /api/v1/translation/urdu/{chapter_id}` - Get cached translation

### Quizzes
- `GET /api/v1/quizzes/{chapter_id}` - Get quiz
- `POST /api/v1/quizzes/{chapter_id}/submit` - Submit answers

## Data Models

### User
- id, name, email, role, software_background, hardware_background

### Chapter
- id, title, module, week, learning_objectives, content

### Quiz
- id, chapter_id, questions (with options and correct answers)

## Testing

### Frontend Tests
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Backend Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_module.py

# Run tests in verbose mode
pytest -v
```

## Deployment

### Local Deployment
```bash
# Build frontend
cd frontend && npm run build

# Deploy with Docker
docker-compose up --build
```

### Production Deployment
1. Set up GitHub Actions workflow
2. Configure production environment variables
3. Push to main branch to trigger deployment
4. Monitor deployment status

## Troubleshooting

### Common Issues

1. **Backend not connecting to Qdrant**
   - Verify QDRANT_URL and QDRANT_API_KEY in .env
   - Check network connectivity to Qdrant cluster

2. **Authentication not working**
   - Verify OAuth client ID and secret
   - Check redirect URIs in OAuth provider configuration

3. **API rate limiting**
   - Check rate limit headers in responses
   - Adjust usage patterns or upgrade API plan

4. **Docker build failures**
   - Ensure Docker is running
   - Check available disk space
   - Verify Dockerfile syntax

### Getting Help
- Check the [documentation](../spec.md) for detailed specifications
- Review the [research](research.md) for technical decisions
- Examine the [data model](data-model.md) for entity relationships
- Consult the [API contracts](contracts/) for integration details

## Next Steps

1. Review the full [implementation plan](plan.md) for sprint breakdown
2. Examine [task definitions](../tasks.md) for development work
3. Explore Claude Code subagents for content generation
4. Set up monitoring and logging for production deployment