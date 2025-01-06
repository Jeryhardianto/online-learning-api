from pydantic import BaseModel
from datetime import datetime
from schemas.common_shcema import BasePage
from typing import List
from enums.enum_tipe import EnrollmentStatus

from utils.util_date_time import convert_datetime_str

class Enroll(BaseModel):
    user_id: int
    course_id : int
    enrolled_date : datetime
    status: EnrollmentStatus
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class EnrollCreate(BaseModel):
    course_id : int
    status: EnrollmentStatus
    enrolled_date: datetime

class EnrollComplate(BaseModel):
    completion_date: datetime
    status: EnrollmentStatus


class OutputEnrollPage(BasePage):
    data: List[Enroll]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }