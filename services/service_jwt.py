
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
import jwt

class ServiceJwt:
 def __init__(self) -> None:
  # openssl rand -hex 32
  self.SECRET_KEY = ("ba7b3a5c286655582178788666f1f1b0069f25960c2e2adcc7626feef86560cc")
  self.ALGORITHM = "HS256"
  self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

 def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
    return encoded_jwt 
 
 def decode_token(self, token: str):
    try:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(401, detail="Invalid credentials")