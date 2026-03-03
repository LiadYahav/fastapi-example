from fastapi import Response, status, Depends, APIRouter
from .. import models, schemas, security
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from ..services import post as post_service

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    dependencies=[Depends(security.get_current_user)]
)


@router.get("/", response_model=List[schemas.PostFull])
async def get_posts(db: AsyncSession = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return await post_service.get_posts(db, limit, skip, search)


@router.get("/{id}", response_model=schemas.PostFull)
async def get_post(id: int, db: AsyncSession = Depends(get_db)):
    return await post_service.get_post_with_votes(db, id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    return await post_service.create_post(db, post, current_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    await post_service.delete_post(db, id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.PostUpdate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    return await post_service.update_post(db, id, post, current_user)
