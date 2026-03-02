from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas


def get_by_id(db: Session, id: int) -> models.Post | None:
    return db.query(models.Post).filter(models.Post.id == id).first()


def get_all_with_votes(db: Session, limit: int, skip: int, search: str):
    query = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id)

    if search:
        query = query.filter(models.Post.title.ilike(f"%{search}%"))

    return query.limit(limit).offset(skip).all()


def get_by_id_with_votes(db: Session, id: int):
    return db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()


def create(db: Session, owner_id: int, post_data: schemas.PostCreate) -> models.Post:
    post = models.Post(owner_id=owner_id, **post_data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update(db: Session, post: models.Post, post_data: schemas.PostUpdate) -> models.Post:
    for key, value in post_data.model_dump().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


def delete(db: Session, post: models.Post) -> None:
    db.delete(post)
    db.commit()
