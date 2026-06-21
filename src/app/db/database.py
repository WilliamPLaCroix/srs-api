from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# -------------------------------------------------
# DATABASE URL
# Swap this later for Postgres in production
# -------------------------------------------------
DATABASE_URL = "sqlite:///./bookwurm.db"


# -------------------------------------------------
# ENGINE
# -------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# -------------------------------------------------
# SESSION FACTORY
# -------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# -------------------------------------------------
# BASE CLASS (SQLAlchemy 2.0 style)
# -------------------------------------------------
class Base(DeclarativeBase):
    pass


# -------------------------------------------------
# FASTAPI DEPENDENCY
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()