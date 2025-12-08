"""
Database configuration and session management
Supports both PostgreSQL (Neon) and SQLite (local development)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - defaults to SQLite for easy local development
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
    # Default to SQLite for local development (no setup required!)
    ASYNC_DATABASE_URL = DEFAULT_SQLITE_URL
    DB_TYPE = "sqlite"

# SQLite-specific settings
connect_args = {}
if DB_TYPE == "sqlite":
    connect_args = {"check_same_thread": False}

# Create async engine
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
