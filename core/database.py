from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:my-secret-password@db.uazzhgvzukwpifcufyfg.supabase.co:5432/postgres"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWT Configuration

SECRET_KEY = "NinnCode6000"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
