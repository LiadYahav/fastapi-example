from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..services import auth as auth_service

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login(db, user_credentials.username, user_credentials.password)
