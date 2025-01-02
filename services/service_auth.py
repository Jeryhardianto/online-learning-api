from fastapi import Depends, HTTPException

from repositories.repository_auth import UserRepositories
from schemas.common_shcema import TokenData
from schemas.user_schema import InputLogin, UserCreate
from services import service_security
from services.service_jwt import ServiceJwt
from sqlalchemy.orm import Session

class ServiceUser:
    def __init__(self, session: Session, service_jwt: ServiceJwt = Depends(ServiceJwt)):
        self.repository_user = UserRepositories(session)
        self.service_security = service_security
        self.service_jwt = service_jwt

    def create_user(self, data: UserCreate):
        is_duplicate_email = self.repository_user.get_user_by_email(data.email)
        if is_duplicate_email is not None:
            raise HTTPException(400, detail="Username already exists")
        
        # Hash password before saving to database
        data.password = self.service_security.get_password_hash(data.password)

        return self.repository_user.store_user(data)
   
    def authenticate_user(self, data: InputLogin):
        found_user = self.repository_user.get_user_by_email(data.email)
        # user not found
        if found_user is None:
            raise HTTPException(401, detail="Invalid username or password")
       
        if not self.service_security.verify_password(data.password, found_user.password):
            raise HTTPException(401, detail="Invalid password")
     
        # Generate JWT token
        jwt_token = self.service_jwt.create_access_token(
            TokenData(id=str(found_user.id), fullname=found_user.fullname).model_dump()
        )
        return jwt_token