from fastapi import APIRouter, status, Depends
from .. import models, schemas, security
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import user as user_service

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, user)


@router.get("/", response_model=list[schemas.UserOut])
async def get_users(db: AsyncSession = Depends(get_db), _current_user: models.User = Depends(security.get_current_user)):
    return await user_service.get_all_users(db)


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db), _current_user: models.User = Depends(security.get_current_user)):
    return await user_service.get_user_or_404(db, id)
