import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configurations
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não definido no .env")

# Engine is responsible for mannager the db connetion
engine = create_engine(DATABASE_URL)

# SessionLocal provides sessions to interact with the db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Defines a basefor models
Base = declarative_base()
