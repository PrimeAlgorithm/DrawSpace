import os
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 

DATABASE_URL = os.getenv("DATABASE_URL") # Get the docker created enviornment variable.

if DATABASE_URL is None:
    raise TypeError("Database URL cannot be None.")

engine = create_engine(DATABASE_URL) # Create the phone line to PostgreSQL.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Session factory - creates individual sessions (workspaces) for each request
Base = declarative_base() # Get the base class we will use to inhert from for our models.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()