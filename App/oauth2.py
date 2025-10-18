from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = '958365f18952a0f56b3179cffbf71df0fe5d0d657d7fab9a3e5b09a01f5df4bc'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=str(username))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)