# dependencies.py
# Get the database session

from database import SessionLocal

def get_sqlite3_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
