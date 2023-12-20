from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD_DATABASE = "my-secret-password"
HOST_URL = "db.uazzhgvzukwpifcufyfg.supabase.co"
PORT = "5432"

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{PASSWORD_DATABASE}@{HOST_URL}:{PORT}/postgres"
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

SECRET_KEY = "QFtGiZPo/eEgYWSxl0Y4mTa+j5+TMUlluP7mXnQ2I1xwy3iSJLxrkGxjdz3o59hdhRwIE2s5T5FpjT7zO5zIHw=="
ALGORITHM = "HS256"
