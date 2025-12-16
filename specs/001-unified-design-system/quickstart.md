# Quickstart: AI-Native Technical Textbook Platform

**Feature**: 001-unified-design-system
**Date**: 2025-12-15 (Updated)

This guide explains how to set up the development environment and run the AI-Native Technical Textbook Platform locally.

---

## Prerequisites

- **Node.js**: v18.x or higher
- **Python**: 3.11 or higher
- **pnpm** or **npm**: Package manager
- **Git**: Version control

### Cloud Services (free tiers)
- **Clerk**: Authentication (create account at clerk.com)
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
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

**Backend** (`backend/.env`):
```env
# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# Qdrant Cloud
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_URL=https://your-cluster.qdrant.io

# Neon Postgres
DATABASE_URL=postgres://user:pass@host/dbname?sslmode=require

# Clerk (for webhook verification)
CLERK_SECRET_KEY=sk_test_...

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000
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
2. Check landing page displays with Dark Blue (#1a1a2e) background
3. Verify Yellow (#ffd700) accents on buttons and CTAs
4. Check statistics cards animate on load
5. Hover over feature cards - verify lift animation with yellow glow

---

## 4. Backend Setup (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database tables
python -c "from src.database.base import init_db; import asyncio; asyncio.run(init_db())"

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

This creates the `textbook_content` collection with chapter embeddings.

---

## 6. Test User Flow

### A. Landing Page (Anonymous)

1. Visit `http://localhost:3000`
2. View hero section with Dark Blue + Yellow theme
3. Check statistics cards (books, users, AI interactions)
4. Click floating chat button
5. Ask a question about Physical AI

### B. Authentication (Clerk)

1. Click "Sign Up" in navbar (top-right)
2. Clerk modal opens with theme-matched styling
3. Complete signup (email/password or social)
4. Get redirected to onboarding form
5. Answer background questions:
   - Software level (beginner/intermediate/advanced)
   - Hardware exposure (none/some/extensive)
   - Robotics experience (none/some/extensive)
6. Profile saved, redirect to textbook

### C. Chatbot with AI Skills

1. Navigate to any chapter page
2. Click "Ask AI" button to open chatbot
3. Ask a whole-book question → Book Content Skill responds
4. Select text in the chapter
5. Click "Ask about selected text" → Context Selection Skill responds
6. Verify typing indicator shows during processing

### D. Personalization

1. While logged in, click "Personalize Content" on a chapter
2. Verify content adapts based on your profile:
   - Beginners see simplified explanations
   - Hardware-experienced users see more technical details
3. Click "Translate to Urdu"
4. Verify Urdu translation displays with RTL direction

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
# No build step - deploy directly to Vercel/Railway
```

---

## Common Issues

### 1. Clerk Auth Not Working
- Verify `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` starts with `pk_`
- Verify `CLERK_SECRET_KEY` starts with `sk_`
- Check Clerk dashboard for application status

### 2. Qdrant Connection Failed
- Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
- Check Qdrant Cloud dashboard for cluster status

### 3. Gemini API Rate Limited
- Check quota in Google AI Studio
- Implement exponential backoff in production

### 4. Neon Connection Issues
- Verify connection string includes `?sslmode=require`
- Check Neon dashboard for connection limits

### 5. CORS Errors
- Ensure `BACKEND_CORS_ORIGINS` includes frontend URL
- Check browser console for specific origin

### 6. Theme Not Displaying Correctly
- Clear browser cache
- Verify CSS variables in `src/css/custom.css`
- Check Dark Blue (#1a1a2e) and Yellow (#ffd700) are applied

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
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
   - `CLERK_SECRET_KEY`
4. Deploy

### Backend (Vercel Functions / Railway)

1. Create new Web Service
2. Set root directory to `backend`
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables:
   - `GEMINI_API_KEY`
   - `QDRANT_API_KEY`
   - `QDRANT_URL`
   - `DATABASE_URL`
   - `CLERK_SECRET_KEY`
6. Deploy

---

## Support

- **Documentation**: `/specs/001-unified-design-system/`
- **API Contracts**: `/specs/001-unified-design-system/contracts/`
- **Data Model**: `/specs/001-unified-design-system/data-model.md`
- **Research**: `/specs/001-unified-design-system/research.md`
