from typing import List
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import ContactResponse, ContactCreate, ContactUpdate
from src.database.db import get_db
from src.services.contacts import ContactService


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> List[ContactResponse]:

    pass


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    pass


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_birthdays_in_next_days(days: int = 7, db: AsyncSession = Depends(get_db)) -> List[ContactResponse]:
    pass


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_by_id(contact_id: int, db: AsyncSession = Depends(get_db)) -> ContactResponse:

    pass


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    pass

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact_data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    pass


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    pass
