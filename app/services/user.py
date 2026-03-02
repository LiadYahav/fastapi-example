from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..repositories import user as user_repo


def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    hashed_password = utils.hash(user_data.password)
    try:
        return user_repo.create(db, user_data.email, hashed_password)
    except Exception as e:
        db.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"email {user_data.email} is already registered")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_user_or_404(db: Session, id: int) -> models.User:
    user = user_repo.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user


def get_all_users(db: Session) -> list[models.User]:
    return user_repo.get_all(db)
