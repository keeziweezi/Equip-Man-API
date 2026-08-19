import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

<<<<<<< HEAD
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgresql:postgresql@localhost:5432/equipment_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
=======
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/equipment_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
>>>>>>> 06fab174fc6b25722a03a0a8cc313224d849f195
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
<<<<<<< HEAD
        db:close() # type: ignore
=======
        db.close()
>>>>>>> 06fab174fc6b25722a03a0a8cc313224d849f195
