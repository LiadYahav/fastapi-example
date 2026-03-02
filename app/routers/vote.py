from fastapi import APIRouter, status, Depends, Response
from .. import models, schemas, security
from ..database import get_db
from sqlalchemy.orm import Session
from ..services import vote as vote_service

router = APIRouter(
    prefix="/vote",
    tags=['Vote'],
    dependencies=[Depends(security.get_current_user)]
)


@router.post("/")
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    result = vote_service.vote(db, vote, current_user)
    if result is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_201_CREATED)
