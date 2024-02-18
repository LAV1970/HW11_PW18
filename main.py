from fastapi import FastAPI, Depends
from . import crud
from pydantic import ContactSerializer, ContactValidator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from typing import List

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


@app.post("/contacts/", response_model=ContactSerializer)
def create_contact(contact: ContactValidator, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact.dict())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
