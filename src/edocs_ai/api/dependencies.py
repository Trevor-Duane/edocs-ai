from collections.abc import Generator

from edocs_ai.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()