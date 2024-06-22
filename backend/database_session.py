# database_session.py
import os
import redis
from database import SessionLocal

# Return the SQLite3 database session
def get_sqlite3_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Return the Redis database session
def get_redis_db():
    # Check if the current environment is in Docker
    is_docker = os.getenv("IS_IN_KCX_BACKEND_DOCKER", "false").lower() == "true"
    
    redis_host = "db-redis" if is_docker else "localhost"
    os.environ["REDIS_HOST"] = redis_host

    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_database = int(os.getenv("REDIS_DB", 0))
    
    redis_client = redis.Redis(host=redis_host, 
                               port=redis_port, 
                               db=redis_database)
    
    return redis_client
