from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, security
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    dependencies=[Depends(security.get_current_user)]
)

def find_post_db(id: int, db: Session) -> models.Post:
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


def update_post_db(id: int, post: schemas.PostUpdate, db: Session) -> models.Post:
    current_post = find_post_db(id, db)

    for key, value in post.model_dump().items():
        setattr(current_post, key, value)

    db.commit()
    db.refresh(current_post)
    return current_post

@router.get("/", response_model=List[schemas.PostFull])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    if search:
        query = query.filter(models.Post.title.ilike(f"%{search}%"))
    posts = query.limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", response_model=schemas.PostFull)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
                models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreate)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    post = find_post_db(id, db)
     
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")


    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostUpdate )
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    updated_post = update_post_db(id, post, db)

    return updated_post

 