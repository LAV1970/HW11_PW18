import crud
from fastapi import FastAPI, Depends
from pydantic import model_serializer, model_validator
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship
from typing import List
from crud import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
)

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    email = Column(String)


# Создаем базу данных
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Создаем сессию базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=model_serializer.Contact)
def create_contact(
    contact: model_validator.ContactCreate, db: Session = Depends(get_db)
):
    return crud.create_contact(db, contact.dict())
