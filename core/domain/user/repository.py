from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models
from core.domain.user import schemas
from core.domain.user.exceptions import EmailAlreadyExistsError
from database.engine import get_db


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_users(self, skip: int = 0, limit: int = 10) -> list[models.User]:
        query = select(models.User).offset(skip).limit(limit)
        result = await self.session.execute(query)
        users = result.scalars().all()
        return users

    async def create_user(self, user: schemas.UserCreate) -> models.User:
        if await self.get_user_by_email(email=user.email):
            raise EmailAlreadyExistsError("Email already taken")

        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password="fakehashed_" + user.password,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def delete_user(self, id: int) -> bool:
        db_user = await self.get_user_by_id(id=id)
        if db_user:
            await self.session.delete(db_user)
            await self.session.commit()
            return True
        return False

    async def get_user_by_id(self, id: int) -> models.User | None:
        stmt = select(models.User).where(models.User.id == id)
        return (await self.session.scalars(stmt)).first()

    async def get_user_by_email(self, email: str) -> models.User | None:
        stmt = select(models.User).where(models.User.email == email)
        return (await self.session.scalars(stmt)).first()

    async def update_user(
        self, id: int, user_update: schemas.UserUpdate
    ) -> models.User:
        db_user = await self.get_user_by_id(id=id)

        if not db_user:
            return None

        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active

        await self.session.commit()
        await self.session.refresh(db_user)

        return db_user
