from datetime import datetime
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from schemas.common_shcema import TokenData
from services.service_common import get_current_user
from sqlalchemy.orm import Session
from services.service_instructor import ServiceInstructor


router = APIRouter(prefix="/instructor", tags=["Instrcutors"])

@router.get("")
async def get_all_instructor(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    page: int = 0,  
    size: int = 10,
    session: Session = Depends(get_db)
):
    service_instructor = ServiceInstructor(session)
    return service_instructor.get_list_instructor(page, size)

@router.get("/{id}")
async def get_instructor_by_id(
    id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_instructor = ServiceInstructor(session)
    return service_instructor.get_by_id(id)

@router.post("")
async def insert_instructor(
   input_instructor: InsructorCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_instructor = ServiceInstructor(session)
  return service_instructor.insert(input_instructor)

@router.put("/{id}")
async def update_instructor(
    id: int,
    input_instructor: InsructorUpdate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_instructor = ServiceInstructor(session)
    return service_instructor.update(id, input_instructor)

@router.delete("/{id}")
async def delete_instructor(
    id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_instructor = ServiceInstructor(session)
    return service_instructor.delete(id)
