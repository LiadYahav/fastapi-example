from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import auth as auth_service

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await auth_service.login(db, user_credentials.username, user_credentials.password)
