from typing import List
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import ContactResponse, ContactCreate, ContactUpdate
from src.database.db import get_db
from src.services.contacts import ContactService


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> List[ContactResponse]:

    service = ContactService(db)
    contacts = await service.get_contacts(skip=skip, limit=limit)

    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contacts found")

    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Query parameter is required")

    service = ContactService(db)
    contacts = await service.search_contacts(query)

    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contacts found. Please check your query.")

    return contacts


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_birthdays_in_next_days(days: int = 7, db: AsyncSession = Depends(get_db)) -> List[ContactResponse]:
    if days <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Days must be a positive integer")

    service = ContactService(db)
    contacts = await service.get_birthdays_in_next_days(days)
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No birthdays found in the next {days} days.")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_by_id(contact_id: int, db: AsyncSession = Depends(get_db)) -> ContactResponse:

    service = ContactService(db)
    contact = await service.get_contact_by_id(contact_id)

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.create_contact(contact)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact_data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    updated_contact = await service.update_contact(contact_id, contact_data)

    if not updated_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return updated_contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    deleted_contact = await service.delete_contact(contact_id)

    if not deleted_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return deleted_contact
