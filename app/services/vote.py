from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..repositories import post as post_repo, vote as vote_repo


def vote(db: Session, vote_data: schemas.Vote, current_user: models.User):
    post = post_repo.get_by_id(db, vote_data.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {vote_data.post_id} was not found")

    existing_vote = vote_repo.get(db, vote_data.post_id, current_user.id)

    if vote_data.direction == 0:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote for post: {vote_data.post_id} was not found for user: {current_user.id}")
        vote_repo.delete(db, existing_vote)
        return None

    else:
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on this post")
        return vote_repo.create(db, vote_data.post_id, current_user.id)
