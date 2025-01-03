from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from config.config import get_db
from schemas.common_shcema import Response, StandardResponse
from schemas.user_schema import InputLogin, OutputLogin, UserCreate
from services.service_auth import ServiceUser
from sqlalchemy.orm import Session
from services.service_jwt import ServiceJwt

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(
  user_input: UserCreate,
  session: Session = Depends(get_db)
):
  service_user = ServiceUser(session)
  service_user.create_user(user_input)
  return Response(success=True, message="User created successfully", data=user_input.dict())


@router.post("/login")
async def login(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  session: Session = Depends(get_db)
):
  
  service_user = ServiceUser(session, service_jwt=ServiceJwt())
  jwt_token = service_user.authenticate_user(InputLogin(email=form_data.username, password=form_data.password))
  return OutputLogin(access_token=jwt_token)