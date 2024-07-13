from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

expiration_time = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    # datetime.utcnow() is deprecated
    expire = datetime.now() + timedelta(minutes=expiration_time)
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
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials", {"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception)