from sqlalchemy import create_engine
from models.classes import Base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

POSTGRES_PORT = os.getenv("db_port")
POSTGRES_PASSWORD = os.getenv("db_password")
POSTGRES_USER = os.getenv("db_username")
POSTGRES_DB = os.getenv("db_name")
POSTGRES_HOST = os.getenv("db_host")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
def create_db_connection():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()