from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from .config import CONFIG

DATABASE_URL = CONFIG["database"]["url"]

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    """Dependency: fornece uma session do SQLAlchemy."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
