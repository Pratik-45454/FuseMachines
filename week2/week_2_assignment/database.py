# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()
logger = get_logger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
        logger.info("Database session opened")
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
        logger.info("Database session closed")