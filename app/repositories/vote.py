from sqlalchemy.orm import Session
from .. import models


def get(db: Session, post_id: int, user_id: int) -> models.Vote | None:
    return db.query(models.Vote).filter(
        models.Vote.post_id == post_id,
        models.Vote.user_id == user_id
    ).first()


def create(db: Session, post_id: int, user_id: int) -> models.Vote:
    vote = models.Vote(post_id=post_id, user_id=user_id)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote


def delete(db: Session, vote: models.Vote) -> None:
    db.delete(vote)
    db.commit()
