# Quickstart: Unified UI/UX + Chatbot Design System

**Feature**: 001-unified-design-system
**Date**: 2025-12-13

This guide explains how to set up the development environment and run the Unified Design System feature locally.

---

## Prerequisites

- **Node.js**: v18.x or higher
- **Python**: 3.11 or higher
- **pnpm** or **npm**: Package manager
- **Git**: Version control

### Cloud Services (free tiers)
- **Qdrant Cloud**: Vector database account
- **Neon**: Serverless Postgres account
- **Google AI Studio**: Gemini API key

---

## 1. Clone Repository

```bash
git clone https://github.com/your-org/physical-ai-course.git
cd physical-ai-course
git checkout 001-unified-design-system
```

---

## 2. Environment Setup

### Create environment files

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** (`backend/.env`):
```env
# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Qdrant Cloud
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_URL=https://your-cluster.qdrant.io

# Neon Postgres
NEON_POSTGRES_URL=postgres://user:pass@host/dbname?sslmode=require

# Better-Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:8000

# CORS
CORS_ORIGINS=http://localhost:3000
```

---

## 3. Frontend Setup (Docusaurus)

```bash
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm start
```

Frontend runs at: `http://localhost:3000`

### Verify Design System

1. Open `http://localhost:3000`
2. Check hero section displays with gradient glow
3. Hover over knowledge cards - verify lift animation
4. Scroll down - verify navbar transition

---

## 4. Backend Setup (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head

# Start development server
uvicorn src.main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`

### Verify Backend

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

---

## 5. Initialize Qdrant Collection

```bash
cd backend

# Index course content into Qdrant
python scripts/index_content.py
```

This creates the `course_content` collection with chapter embeddings.

---

## 6. Test User Flow

### A. Landing Page (Anonymous)

1. Visit `http://localhost:3000`
2. View hero section, animated cards, roadmap
3. Click floating chat button
4. Ask a question about Physical AI

### B. Authentication

1. Click "Sign Up" in navbar
2. Enter email and password
3. Complete profile setup (skill level, language preference)
4. Verify redirect to dashboard

### C. Chatbot with Context

1. Navigate to a chapter page
2. Select text in the chapter
3. Click "Ask about selected text"
4. Verify chatbot opens with context indicator
5. Send message and receive AI response

### D. Personalization

1. While logged in, click "Personalize" on a chapter
2. Verify content adapts to your skill level
3. Toggle "Translate to Urdu"
4. Verify Urdu translation displays

---

## 7. Run Tests

### Frontend Tests
```bash
cd frontend
pnpm test
```

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Contract Tests
```bash
cd backend
pytest tests/contract/ -v
```

---

## 8. Build for Production

### Frontend
```bash
cd frontend
pnpm build
# Output: frontend/build/
```

### Backend
```bash
cd backend
# No build step - deploy directly to Render/Railway
```

---

## Common Issues

### 1. Qdrant Connection Failed
- Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
- Check Qdrant Cloud dashboard for cluster status

### 2. Gemini API Rate Limited
- Check quota in Google AI Studio
- Implement exponential backoff in production

### 3. Neon Connection Issues
- Verify connection string includes `?sslmode=require`
- Check Neon dashboard for connection limits

### 4. CORS Errors
- Ensure `CORS_ORIGINS` includes frontend URL
- Check browser console for specific origin

### 5. Animations Not Rendering
- Verify Framer Motion installed: `pnpm list framer-motion`
- Check browser supports CSS transforms

---

## Development Workflow

1. **Create branch**: `git checkout -b feature/your-feature`
2. **Make changes**: Edit components, add tests
3. **Run tests**: `pnpm test` / `pytest`
4. **Commit**: Follow conventional commits
5. **Push**: `git push origin feature/your-feature`
6. **PR**: Create pull request to `001-unified-design-system`

---

## Deployment

### Frontend (Vercel)

1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Set environment variables in Vercel dashboard
4. Deploy

### Backend (Render)

1. Create new Web Service on Render
2. Set root directory to `backend`
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables
6. Deploy

---

## Support

- **Documentation**: `/specs/001-unified-design-system/`
- **API Contracts**: `/specs/001-unified-design-system/contracts/`
- **Data Model**: `/specs/001-unified-design-system/data-model.md`
