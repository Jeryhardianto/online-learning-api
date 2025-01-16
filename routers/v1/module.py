from datetime import datetime
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from schemas.common_shcema import TokenData
from schemas.module_schema import ModuleCreate, ModuleUpdate
from services.service_common import get_current_user
from sqlalchemy.orm import Session
from services.service_module import ServiceModule


router = APIRouter(prefix="/module", tags=["Modules"])

@router.get("/{course_id}/course")
async def get_modules(
   course_id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   page: int = 0,  
   size: int = 10,
   session: Session = Depends(get_db)
):
  service_module = ServiceModule(session)
  return service_module.get_all(page, size, course_id)

@router.post("/{course_id}/course")
async def insert_module(
   course_id: int,
   input_module: ModuleCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_module = ServiceModule(session)
  return service_module.insert(input_module, course_id)

@router.put("/{id}/course/{course_id}")
async def update_module(
   id: int,
   course_id: int,
   input_module: ModuleUpdate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_module = ServiceModule(session)
  return service_module.update(input_module, course_id, id)

@router.delete("/{id}/course/{course_id}")
async def delete_module(
   id: int,
   course_id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_module = ServiceModule(session)
  return service_module.delete(id, course_id)
