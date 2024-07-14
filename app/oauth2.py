from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import schemas, database, models
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

expiration_time = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    # datetime.utcnow() is deprecated
    expire = datetime.now() + timedelta(minutes=settings.jwt_expiration)
    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return access_token

def verify_access_token(token: str, credentials_exception):
    try:
        token = token.strip()
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm)
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)) -> models.User:
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", {"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        # valid token but user record is not in db
        raise HTTPException(status.HTTP_404_NOT_FOUND, "authenticated user not found")        
    return user