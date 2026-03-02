from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, utils, security, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
         
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = security.create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}