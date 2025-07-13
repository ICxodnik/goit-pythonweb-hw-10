import asyncio
import random
from faker import Faker

from src.services.auth import Hash
from src.services.users import UserService
from src.database.db import sessionmanager
from src.schemas import ContactCreate, User, UserCreate
from src.services.contacts import ContactService
from src.repository.contacts import ContactRepository

fake = Faker()


def generate_valid_phone():
    while True:
        phone = fake.phone_number()
        clean_phone = ''.join(c for c in phone if c.isdigit() or c in '+- ')
        if len(clean_phone) <= 15:
            return clean_phone


async def seed_contacts(count: int = 10, users: list[User] = []):
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
            await service.create_contact(contact_data, users[random.randint(0, len(users) - 1)])

        await session.commit()
        
async def seed_users(count: int = 10):
    users = []
    async with sessionmanager.session() as session:
        for _ in range(count):
            user_service = UserService(session)
            user_data = UserCreate(
                username=fake.user_name(),
                email=fake.unique.email(),
                password="123456",
                is_verified=True,
            )

            user_data.password = Hash().get_password_hash(user_data.password)
            new_user = await user_service.create_user(user_data)
            users.append(new_user)
    return users


async def main():
    users = await seed_users(10)
    await seed_contacts(100, users)


if __name__ == "__main__":
    asyncio.run(main())
