from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD_DATABASE = os.getenv("PASSWORD_DATABASE")
HOST_URL = os.getenv("HOST_URL")
PORT = os.getenv("PORT")

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

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
