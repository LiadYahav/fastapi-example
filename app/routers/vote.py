from fastapi import APIRouter, status, HTTPException, Depends, Response
from .. import models, schemas, utils, security
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote'],
    dependencies=[Depends(security.get_current_user)]
)


  
@router.post("/")
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    
    post_found = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {vote.post_id} was not found")

    vote_found = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first()

    if vote.direction == 0:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote for post: {vote.post_id} was not found for user: {current_user.id  }") 
        db.delete(vote_found)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on this post")

        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)

        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        return Response(status_code=status.HTTP_201_CREATED)