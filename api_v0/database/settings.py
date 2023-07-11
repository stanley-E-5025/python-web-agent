from sqlmodel import SQLModel, create_engine
from .models import User  # import your models here

DATABASE_URL = "sqlite:///./database.sqlite3"
engine = create_engine(DATABASE_URL)

def create_tables():
    SQLModel.metadata.create_all(engine)

