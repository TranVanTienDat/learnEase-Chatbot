import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

# Biến toàn cục cache engine & session factory
_engine = None
_SessionLocal = None

def get_db_credentials():
    return {
        "user": os.getenv("DATABASE_USERNAME"),
        "password": os.getenv("DATABASE_PASSWORD"),
        "host": os.getenv("DATABASE_HOST"),
        "port": int(os.getenv("DATABASE_PORT", 5432)),
        "db": os.getenv("DATABASE_NAME"),
    }

def get_engine():
    global _engine
    if _engine is None:
        creds = get_db_credentials()
        url = URL.create(
            drivername="postgresql+psycopg2",
            username=creds["user"],
            password=creds["password"],  # KHÔNG cần encode
            host=creds["host"],
            port=creds["port"],
            database=creds["db"]
        )

        _engine = create_engine(url, pool_pre_ping=True)
    return _engine

def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
    return _SessionLocal()

def test_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1")) 
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {str(e)}")
        return False