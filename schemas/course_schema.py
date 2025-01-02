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
    price: float
    difiiculty: str
    is_published: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title: str
    description: str
    instructor_id: int
    price: float
    difiiculty: DifficultyLevel
    is_published: int

class TodoUpdate(BaseModel):
    title: str
    description: str
    instructor_id: int
    price: float
    difiiculty: DifficultyLevel
    is_published: int

class OutputTransactionPage(BasePage):
    data: List[Course]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }