from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schemas, utils, security
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

def find_user_db(id: int, db: Session) -> models.User:
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    user_data["password"] = utils.hash(user_data["password"])

    new_user = models.User(**user_data)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"email {user.email} is already registered")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_user

@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), _current_user: models.User = Depends(security.get_current_user)):
    users = db.query(models.User).all()

    return users

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), _current_user: models.User = Depends(security.get_current_user)):
    user = find_user_db(id, db)

    return user