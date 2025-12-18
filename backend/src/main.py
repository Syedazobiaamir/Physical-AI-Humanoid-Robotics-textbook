"""
Main FastAPI application for Physical AI & Humanoid Robotics Textbook Platform

This module serves as the entry point for both local development and Vercel deployment.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import sys

# Ensure the src directory is in the Python path for Vercel deployment
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Load environment variables (optional for Vercel - uses env vars directly)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required in production

# Import database initialization
try:
    from .database.base import init_db, get_db_info
except ImportError:
    from src.database.base import init_db, get_db_info

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database tables
    try:
        await init_db()
        db_info = get_db_info()
        print(f"Database initialized: {db_info['type']} - configured: {db_info['is_configured']}")
    except Exception as e:
        print(f"Warning: Database initialization skipped: {e}")
    yield
    # Shutdown: cleanup if needed
    pass

# Create FastAPI app with lifespan
app = FastAPI(
    title="Physical AI & Humanoid Robotics API",
    description="Backend API for the AI-native textbook platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS - include Vercel domains and localhost
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.vercel.app",
]
env_origins = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")
origins = list(default_origins)
for origin in env_origins:
    stripped_origin = origin.strip()
    if stripped_origin and stripped_origin not in origins:
        origins.append(stripped_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use the dynamically constructed origins list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Physical AI & Humanoid Robotics API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
        "platform": "Vercel" if os.getenv("VERCEL") else "local"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    db_info = get_db_info()
    return {
        "status": "healthy",
        "service": "physical-ai-api",
        "database": {
            "type": db_info["type"],
            "configured": db_info["is_configured"]
        }
    }

# API v1 routes - using try/except for import flexibility
try:
    # Try relative imports first (for local development with package structure)
    from .api import content, rag, auth, personalization, progress, translation, quizzes, stats, user
except ImportError:
    # Fall back to absolute imports (for Vercel deployment)
    from src.api import content, rag, auth, personalization, progress, translation, quizzes, stats, user

app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(personalization.router, prefix="/api/v1/personalization", tags=["Personalization"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(translation.router, prefix="/api/v1/translation", tags=["Translation"])
app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["Quizzes"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["Statistics"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
