import asyncio
from faker import Faker

from src.database.db import sessionmanager
from src.schemas import ContactCreate
from src.services.contacts import ContactService
from src.repository.contacts import ContactRepository

fake = Faker()


def generate_valid_phone():
    while True:
        phone = fake.phone_number()
        clean_phone = ''.join(c for c in phone if c.isdigit() or c in '+- ')
        if len(clean_phone) <= 15:
            return clean_phone


async def seed_contacts(count: int = 10):
    async with sessionmanager.session() as session:
        repo = ContactRepository(session)
        service = ContactService(session)

        existing = await repo.get_contacts_count()
        if existing > 0:
            print("Contacts already exist. Skipping seeding.")
            return

        for _ in range(count):
            contact_data = ContactCreate(
                name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=generate_valid_phone(),
                birthday=fake.date_of_birth(minimum_age=18, maximum_age=90),
                additional_info=fake.sentence(nb_words=6),
            )
            await service.create_contact(contact_data)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_contacts(100))
