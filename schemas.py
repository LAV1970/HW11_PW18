from pydantic import BaseModel


class ContactBase(BaseModel):
    name: str
    phone: str
    email: str
    birthday: str


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
