from fastapi import APIRouter, status, Depends, Response
from .. import models, schemas, security
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import vote as vote_service

router = APIRouter(
    prefix="/vote",
    tags=['Vote'],
    dependencies=[Depends(security.get_current_user)]
)


@router.post("/")
async def vote(vote: schemas.Vote, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    result = await vote_service.vote(db, vote, current_user)
    if result is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_201_CREATED)
