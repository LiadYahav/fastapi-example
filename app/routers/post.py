from fastapi import Response, status, Depends, APIRouter
from .. import models, schemas, security
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from ..services import post as post_service

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    dependencies=[Depends(security.get_current_user)]
)


@router.get("/", response_model=List[schemas.PostFull])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return post_service.get_posts(db, limit, skip, search)


@router.get("/{id}", response_model=schemas.PostFull)
def get_post(id: int, db: Session = Depends(get_db)):
    return post_service.get_post_with_votes(db, id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    return post_service.create_post(db, post, current_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    post_service.delete_post(db, id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    return post_service.update_post(db, id, post, current_user)
