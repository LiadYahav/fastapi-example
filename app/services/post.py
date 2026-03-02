from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..repositories import post as post_repo


def get_posts(db: Session, limit: int, skip: int, search: str):
    return post_repo.get_all_with_votes(db, limit, skip, search)


def get_post_with_votes(db: Session, id: int):
    post = post_repo.get_by_id_with_votes(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


def create_post(db: Session, post_data: schemas.PostCreate, current_user: models.User) -> models.Post:
    return post_repo.create(db, current_user.id, post_data)


def update_post(db: Session, id: int, post_data: schemas.PostUpdate, current_user: models.User) -> models.Post:
    post = post_repo.get_by_id(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")
    return post_repo.update(db, post, post_data)


def delete_post(db: Session, id: int, current_user: models.User) -> None:
    post = post_repo.get_by_id(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")
    post_repo.delete(db, post)
