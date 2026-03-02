from sqlalchemy.orm import Session
from .. import models


def get_by_id(db: Session, id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == id).first()


def get_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_all(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def create(db: Session, email: str, hashed_password: str) -> models.User:
    user = models.User(email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
