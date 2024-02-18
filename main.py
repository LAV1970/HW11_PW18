from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
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


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ContactValidator(BaseModel):
    name: str
    phone: str
    email: str


# Ручка для создания нового контакта
@app.post("/contacts/", response_model=ContactValidator)
def create_contact(contact: ContactValidator, db: Session = Depends(get_db)):
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


# Ручка для получения списка всех контактов
@app.get("/contacts/", response_model=List[ContactValidator])
def get_all_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


# Ручка для получения одного контакта по идентификатору
@app.get("/contacts/{contact_id}", response_model=ContactValidator)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# Ручка для обновления существующего контакта
@app.put("/contacts/{contact_id}", response_model=ContactValidator)
def update_contact(
    contact_id: int, updated_contact: ContactValidator, db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    for field, value in updated_contact.dict().items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)
    return contact


# Ручка для удаления контакта
@app.delete("/contacts/{contact_id}", response_model=ContactValidator)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return contact


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
