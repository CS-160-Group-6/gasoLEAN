from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.config import settings

# Create the SQLAlchemy engine using the database URL from settings
# This is what will be used by SQLAlchemy Session to connect to
# the database
engine: Engine = create_engine(
    url=settings.DB_URL,
    connect_args={"check_same_thread": False}, # Required for SQLite to allow multiple threads
    pool_pre_ping=True, # Enable pre-ping to check connection health
    echo=True  # SQL query logging
)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(
    autocommit = False, # Disable autocommit mode so that we can control transactions manually
    autoflush = False, # Disable autoflush mode
    bind = engine # Bind the session to the engine
)

def get_db() -> Generator[Session, Any, None]:
    """
    Dependency that provides a database session.

    This function is used in FastAPI routes to get a database session.
    It ensures that the session is properly closed after use.
    """
    db: Session = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session for use in the route
    finally:
        db.close()  # Close the session when done