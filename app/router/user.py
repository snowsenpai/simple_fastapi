from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payload: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(payload.password)
    payload.password = hashed_password
    
    user = models.User(**payload.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"user with id '{id}' does not exist")
    return user

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"user with id '{id}' does not exist")
    user_query.delete(synchronize_session=False)
    db.commit()

    return {"message": f"user with id {id} has been deleted"}