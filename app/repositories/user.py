from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models


async def get_by_id(db: AsyncSession, id: int) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.id == id))
    return result.scalar_one_or_none()


async def get_by_email(db: AsyncSession, email: str) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


async def get_all(db: AsyncSession) -> list[models.User]:
    result = await db.execute(select(models.User))
    return list(result.scalars().all())


async def create(db: AsyncSession, email: str, hashed_password: str) -> models.User:
    user = models.User(email=email, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
