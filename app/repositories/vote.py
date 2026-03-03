from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models


async def get(db: AsyncSession, post_id: int, user_id: int) -> models.Vote | None:
    result = await db.execute(
        select(models.Vote).where(
            models.Vote.post_id == post_id,
            models.Vote.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, post_id: int, user_id: int) -> models.Vote:
    vote = models.Vote(post_id=post_id, user_id=user_id)
    db.add(vote)
    await db.commit()
    await db.refresh(vote)
    return vote


async def delete(db: AsyncSession, vote: models.Vote) -> None:
    await db.delete(vote)
    await db.commit()
