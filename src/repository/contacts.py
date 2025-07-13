from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int = 0, limit: int = 10) -> List[ContactModel]:
        query = select(Contact).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> ContactResponse | None:
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, contact: ContactModel) -> ContactModel:
        result = Contact(**contact.model_dump())
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return await self.get_contact_by_id(result.id)

    async def update_contact(self, contact_id: int, contact_data: ContactUpdate) -> ContactResponse | None:
        q_contact = await self.get_contact_by_id(contact_id)

        if q_contact:
            update_data = contact_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(q_contact, field, value)

            await self.db.commit()
            await self.db.refresh(q_contact)

        return await self.get_contact_by_id(contact_id)

    async def delete_contact(self, contact_id: int) -> ContactModel | None:
        q_contact = await self.get_contact_by_id(contact_id)
        if q_contact:
            await self.db.delete(q_contact)
            await self.db.commit()

        return q_contact

    async def search_contacts(self, query: str) -> List[ContactResponse]:

        stmt = select(Contact).where(
            (Contact.name.ilike(f'%{query}%')) |
            (Contact.last_name.ilike(f'%{query}%')) |
            (Contact.email.ilike(f'%{query}%'))
        )
        result = await self.db.execute(stmt)
        contacts = result.scalars().all()

        return [ContactResponse.model_validate(contact) for contact in contacts]

    async def get_birthdays(self, days: int) -> List[ContactResponse]:
        today = datetime.today()
        end = today + timedelta(days=days)
        days_range = [
            (today + timedelta(days=i)).strftime("%m-%d")
            for i in range((end - today).days + 1)
        ]
        birthday_days = func.to_char(Contact.birthday, "MM-DD")
        stmt = select(Contact).where(birthday_days.in_(days_range))
        result = await self.db.execute(stmt)
        contacts = result.scalars().all()

        return [ContactResponse.model_validate(contact) for contact in contacts]

    async def get_contacts_count(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Contact))
        return result.scalar_one()
