from datetime import datetime
from typing import Optional
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from enums.enum_tipe import IsDone
from schemas.common_shcema import TokenData
from schemas.todo_schema import OutputTransactionPage, TodoCreate, TodoIsDone, TodoUpdate
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

# @router.post("")
# def insert_todo(
#    input_todo: TodoCreate,
#    current_user: Annotated[TokenData, Depends(get_current_user)],
#    session: Session = Depends(get_db)
# ):
#   service_course = ServiceCourse(session)
#   return service_course.insert(input_todo, current_user)

# @router.put("/{id}")
# def update_todo(
#     id: int,
#     input_todo: TodoUpdate,
#     current_user: Annotated[TokenData, Depends(get_current_user)],
#     session: Session = Depends(get_db)
# ):
#     service_course = ServiceCourse(session)
#     return service_course.update(id, input_todo, current_user)

# @router.patch("/{id}/is_done")
# def is_done_todo(
#     id: int,
#     input_todo: TodoIsDone,
#     current_user: Annotated[TokenData, Depends(get_current_user)],
#     session: Session = Depends(get_db)
# ):
#     service_course = ServiceCourse(session)
#     return service_course.is_done(id, input_todo, current_user)

# @router.delete("/{id}")
# def delete_todo(
#     id: int,
#     current_user: Annotated[TokenData, Depends(get_current_user)],
#     session: Session = Depends(get_db)
# ):
#     service_course = ServiceCourse(session)
#     return service_course.delete(id, current_user)
