from datetime import datetime
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from schemas.common_shcema import TokenData
from schemas.enroll_schema import EnrollComplate, EnrollCreate
from services.service_common import get_current_user
from sqlalchemy.orm import Session
from services.service_enroll import ServiceEnrroll


router = APIRouter(prefix="/enrollment", tags=["Enrollments"])

@router.get("")
async def get_all_enroll(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    page: int = 0,  
    size: int = 10,
    session: Session = Depends(get_db)
):
    service_enrollment = ServiceEnrroll(session)
    return service_enrollment.get_list_enroll(page, size, current_user)

@router.post("")
async def insert_enroll(
   input_enroll: EnrollCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_enrollment = ServiceEnrroll(session)
  return service_enrollment.insert(input_enroll, current_user)

@router.patch("/{course_id}")
async def complate_enroll(
    course_id: int,
    input_enroll: EnrollComplate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Session = Depends(get_db)
):
   service_enrollment = ServiceEnrroll(session)
   return service_enrollment.complate(course_id, input_enroll, current_user)
