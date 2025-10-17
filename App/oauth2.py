from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY

SECRET_KEY = '958365f18952a0f56b3179cffbf71df0fe5d0d657d7fab9a3e5b09a01f5df4bc'

# ALGORITHM = "HS256"
ALGORITHM = 'HS256'

# EXPIRATION_TIME_MINUTES = 30
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    