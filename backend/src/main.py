"""
Main FastAPI application for Physical AI & Humanoid Robotics Textbook Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics API",
    description="Backend API for the AI-native textbook platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "physical-ai-api"
    }

# API v1 routes
from .api import content, rag, auth, personalization, progress, translation, quizzes

app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(personalization.router, prefix="/api/v1/personalization", tags=["Personalization"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(translation.router, prefix="/api/v1/translation", tags=["Translation"])
app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["Quizzes"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
