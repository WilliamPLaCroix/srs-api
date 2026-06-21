import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from app.db.database import get_engine


def test_db_connection():
    engine = get_engine()

    try:
        with engine.connect() as conn:
            assert conn.execute(text("SELECT 1")).scalar() == 1
    except OperationalError:
        pytest.skip("Database not available")