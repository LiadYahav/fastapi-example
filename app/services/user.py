from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas, utils
from ..repositories import user as user_repo


async def create_user(db: AsyncSession, user_data: schemas.UserCreate) -> models.User:
    hashed_password = await utils.hash(user_data.password)
    try:
        return await user_repo.create(db, user_data.email, hashed_password)
    except Exception as e:
        await db.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"email {user_data.email} is already registered")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def get_user_or_404(db: AsyncSession, id: int) -> models.User:
    user = await user_repo.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user


async def get_all_users(db: AsyncSession) -> list[models.User]:
    return await user_repo.get_all(db)
