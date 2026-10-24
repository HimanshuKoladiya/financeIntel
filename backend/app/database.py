import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger("financeintel.database")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./financeintel.db"

try:
    if DATABASE_URL.startswith("postgresql"):
        # Test connection with a 2-second timeout
        test_engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 2}, pool_pre_ping=True)
        with test_engine.connect():
            pass
        engine = test_engine
    else:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
except Exception as e:
    logger.warning("Postgres unavailable (%s). Using local SQLite database.", e)
    DATABASE_URL = "sqlite:///./financeintel.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

