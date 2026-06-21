import pytest
from sqlalchemy import text

from app.db.database import engine, SessionLocal, get_db, Base
Base.metadata.create_all(bind=engine)

def test_engine_exists():
    assert engine is not None


def test_session_creation():
    db = SessionLocal()
    assert db is not None
    db.close()


def test_db_connection_smoke():
    # works for sqlite; adjust later for postgres CI
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_db_dependency():
    gen = get_db()
    db = next(gen)
    assert db is not None
    try:
        next(gen)
    except StopIteration:
        pass