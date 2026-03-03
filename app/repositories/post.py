from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .. import models, schemas


async def get_by_id(db: AsyncSession, id: int) -> models.Post | None:
    result = await db.execute(
        select(models.Post).where(models.Post.id == id)
    )
    return result.scalar_one_or_none()


async def get_all_with_votes(db: AsyncSession, limit: int, skip: int, search: str):
    query = select(
        models.Post, func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).options(selectinload(models.Post.owner))

    if search:
        query = query.where(models.Post.title.ilike(f"%{search}%"))

    result = await db.execute(query.limit(limit).offset(skip))
    return result.all()


async def get_by_id_with_votes(db: AsyncSession, id: int):
    result = await db.execute(
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .where(models.Post.id == id)
        .options(selectinload(models.Post.owner))
    )
    return result.first()


async def create(db: AsyncSession, owner_id: int, post_data: schemas.PostCreate) -> models.Post:
    post = models.Post(owner_id=owner_id, **post_data.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    await db.refresh(post, attribute_names=['owner'])
    return post


async def update(db: AsyncSession, post: models.Post, post_data: schemas.PostUpdate) -> models.Post:
    for key, value in post_data.model_dump().items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    await db.refresh(post, attribute_names=['owner'])
    return post


async def delete(db: AsyncSession, post: models.Post) -> None:
    await db.delete(post)
    await db.commit()
