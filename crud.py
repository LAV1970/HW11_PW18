from sqlalchemy.orm import Session
from main import Contact


def create_contact(db: Session, contact_data: dict):
    contact = Contact(**contact_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
