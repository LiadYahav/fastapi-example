from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import utils, security
from ..repositories import user as user_repo


def login(db: Session, email: str, password: str) -> dict:
    user = user_repo.get_by_email(db, email)

    if not user or not utils.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
