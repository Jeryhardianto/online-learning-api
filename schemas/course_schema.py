from pydantic import BaseModel
from datetime import datetime
from enums.enum_tipe import DifficultyLevel
from schemas.common_shcema import BasePage
from typing import List

from utils.util_date_time import convert_datetime_str

class Course(BaseModel):
    title: str
    description: str
    instructor_id: int
    image: str | None
    price: float
    difiiculty: str
    is_published: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str
    description: str
    instructor_id: int
    price: float
    difiiculty: DifficultyLevel
    is_published: int

class CourseUpdate(BaseModel):
    title: str
    description: str
    instructor_id: int
    price: float
    difiiculty: DifficultyLevel
    is_published: int

class CourseImage(BaseModel):
    id : int
    image: str
    class Config:
        from_attributes = True

class OutputCoursePage(BasePage):
    data: List[Course]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }