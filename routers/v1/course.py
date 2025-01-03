from datetime import datetime
from typing import Optional, List
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, UploadFile

from config.config import get_db
from schemas.course_schema import CourseCreate, CourseUpdate
from schemas.common_shcema import TokenData
from services.service_common import get_current_user
from sqlalchemy.orm import Session
from services.service_course import ServiceCourse


router = APIRouter(prefix="/course", tags=["Courses"])

@router.get("")
async def get_all_todo(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    page: int = 0,
    size: int = 10,
    session: Session = Depends(get_db)
):
    service_course = ServiceCourse(session)
    return service_course.get_list_course(page, size)

@router.get("/{id}")
async def get_course_by_id(
    id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_course = ServiceCourse(session)
    return service_course.get_by_id(id)

@router.post("")
async def insert_course(
   input_course: CourseCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_course = ServiceCourse(session)
  return service_course.insert(input_course)

@router.put("/{id}")
def update_todo(
    id: int,
    input_course: CourseUpdate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_course = ServiceCourse(session)
    return service_course.update(id, input_course)

@router.post("/{id}/upload_image")
def upload_image(
    id: int,
    image: UploadFile,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_course = ServiceCourse(session)
    return service_course.upload_image(id, image)

@router.delete("/{id}")
def delete_todo(
    id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
    service_course = ServiceCourse(session)
    return service_course.delete(id)
