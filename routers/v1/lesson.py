from datetime import datetime
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from schemas.common_shcema import TokenData
from schemas.lesson_schema import LessonCreate, LessonUpdate
from services.service_common import get_current_user
from sqlalchemy.orm import Session
from services.service_lesson import ServiceLesson
from services.service_module import ServiceModule


router = APIRouter(prefix="/lesson", tags=["Lessons"])

@router.get("/{module_id}/lesson")
async def get_modules(
   module_id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   page: int = 0,  
   size: int = 10,
   session: Session = Depends(get_db)
):
  service_lesson = ServiceLesson(session)
  return service_lesson.get_all(page, size, module_id)

@router.post("/{module_id}")
async def insert_lesson(
   module_id: int,
   input_lesson: LessonCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_lesson = ServiceLesson(session)
  return service_lesson.insert(input_lesson, module_id)

@router.put("/{id}/module/{module_id}")
async def update_lesson(
   id: int,
   module_id: int,
   input_lesson: LessonUpdate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_lesson = ServiceLesson(session)
  return service_lesson.update(input_lesson, module_id, id)

# @router.delete("/{id}/course/{course_id}")
# async def delete_module(
#    id: int,
#    course_id: int,
#    current_user: Annotated[TokenData, Depends(get_current_user)],
#    session: Session = Depends(get_db)
# ):
#   service_module = ServiceModule(session)
#   return service_module.delete(id, course_id)
