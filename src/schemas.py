from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class ContactModel(BaseModel):

    name: str = Field(max_length=30, min_length=3)
    last_name: str = Field(max_length=50, min_length=1)
    email: EmailStr
    phone: str = Field(max_length=15, min_length=7)
    birthday: date
    additional_info: Optional[str] = Field(max_length=255, default=None)


class ContactCreate(ContactModel):
    pass


class ContactUpdate(ContactModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None


class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
