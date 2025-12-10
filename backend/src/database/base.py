"""
Database configuration and session management
Supports both PostgreSQL (Neon) and SQLite (local development)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os

# Load environment variables (optional - Vercel uses env vars directly)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required in production

# Check if we're on Vercel (read-only filesystem)
IS_VERCEL = os.getenv("VERCEL", "").lower() in ("1", "true")

# Database URL - defaults to in-memory SQLite for serverless
# Use in-memory SQLite for Vercel to avoid filesystem issues
if IS_VERCEL:
    DEFAULT_SQLITE_URL = "sqlite+aiosqlite:///:memory:"
else:
    DEFAULT_SQLITE_URL = "sqlite+aiosqlite:///./physical_ai_textbook.db"

DATABASE_URL = os.getenv("DATABASE_URL", "")
NEON_DB_URL = os.getenv("NEON_DB_URL", "")

# Determine which database to use
if NEON_DB_URL:
    # Use Neon PostgreSQL if configured
    ASYNC_DATABASE_URL = NEON_DB_URL.replace("postgresql://", "postgresql+asyncpg://")
    DB_TYPE = "postgresql"
elif DATABASE_URL:
    # Use configured DATABASE_URL
    if DATABASE_URL.startswith("postgresql://"):
        ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        DB_TYPE = "postgresql"
    elif DATABASE_URL.startswith("sqlite"):
        ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
        DB_TYPE = "sqlite"
    else:
        ASYNC_DATABASE_URL = DATABASE_URL
        DB_TYPE = "unknown"
else:
    # Default to SQLite (in-memory for Vercel, file for local)
    ASYNC_DATABASE_URL = DEFAULT_SQLITE_URL
    DB_TYPE = "sqlite"

# SQLite-specific settings
connect_args = {}
if DB_TYPE == "sqlite":
    connect_args = {"check_same_thread": False}

# Create async engine with error handling
try:
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=os.getenv("DEBUG", "false").lower() == "true",
        future=True,
        connect_args=connect_args if DB_TYPE == "sqlite" else {}
    )

    # Create async session factory
    AsyncSessionLocal = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
except Exception as e:
    # If database initialization fails, create a dummy engine
    # This allows the app to start and return errors gracefully
    print(f"Warning: Database initialization failed: {e}")
    async_engine = None
    AsyncSessionLocal = None

# Base class for models
Base = declarative_base()


# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Initialize database tables
async def init_db():
    """Create all tables - call this on startup"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_db_info() -> dict:
    """Get current database configuration info"""
    return {
        "type": DB_TYPE,
        "url": ASYNC_DATABASE_URL.split("@")[-1] if "@" in ASYNC_DATABASE_URL else ASYNC_DATABASE_URL,
        "is_configured": bool(NEON_DB_URL or DATABASE_URL)
    }
