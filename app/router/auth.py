from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/auth", tags=['Auth'])

@router.post("/login")
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.username).first()
    invalid_credentials = HTTPException(status.HTTP_403_FORBIDDEN, "invalid credentials")
    if not user:
        raise invalid_credentials
    if not utils.verify(payload.password, user.password):
        raise invalid_credentials
    # create token
    access_token = oauth2.create_access_token({"user_id": user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}