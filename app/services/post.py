from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas
from ..repositories import post as post_repo


async def get_posts(db: AsyncSession, limit: int, skip: int, search: str):
    return await post_repo.get_all_with_votes(db, limit, skip, search)


async def get_post_with_votes(db: AsyncSession, id: int):
    post = await post_repo.get_by_id_with_votes(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


async def create_post(db: AsyncSession, post_data: schemas.PostCreate, current_user: models.User) -> models.Post:
    return await post_repo.create(db, current_user.id, post_data)


async def update_post(db: AsyncSession, id: int, post_data: schemas.PostUpdate, current_user: models.User) -> models.Post:
    post = await post_repo.get_by_id(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")
    return await post_repo.update(db, post, post_data)


async def delete_post(db: AsyncSession, id: int, current_user: models.User) -> None:
    post = await post_repo.get_by_id(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")
    await post_repo.delete(db, post)
