from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import models
from core.domain.user import schemas
from core.domain.user.exceptions import EmailAlreadyExistsError


async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[models.User]:
    query = select(models.User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    if await get_user_by_email(db=db, email=user.email):
        raise EmailAlreadyExistsError("Email already taken")

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password="fakehashed_" + user.password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, id: int) -> bool:
    db_user = await get_user_by_id(db=db, id=id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False


async def get_user_by_id(id: int, db: AsyncSession) -> models.User | None:
    stmt = select(models.User).where(models.User.id == id)
    return (await db.scalars(stmt)).first()


async def get_user_by_email(email: str, db: AsyncSession) -> models.User | None:
    stmt = select(models.User).where(models.User.email == email)
    return (await db.scalars(stmt)).first()


async def update_user(
    db: AsyncSession, id: int, user_update: schemas.UserUpdate
) -> models.User:
    db_user = await get_user_by_id(db=db, id=id)

    if not db_user:
        return None

    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active

    await db.commit()
    await db.refresh(db_user)

    return db_user
