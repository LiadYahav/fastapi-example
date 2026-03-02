from fastapi import APIRouter, status, Depends
from .. import models, schemas, security
from ..database import get_db
from sqlalchemy.orm import Session
from ..services import user as user_service

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), _current_user: models.User = Depends(security.get_current_user)):
    return user_service.get_all_users(db)


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), _current_user: models.User = Depends(security.get_current_user)):
    return user_service.get_user_or_404(db, id)
