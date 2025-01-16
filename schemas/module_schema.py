from pydantic import BaseModel
from datetime import datetime
from enums.enum_tipe import DifficultyLevel
from schemas.common_shcema import BasePage
from typing import List

from utils.util_date_time import convert_datetime_str

class Module(BaseModel):
    course_id: int
    title: str
    description: str
    sequence_number: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ModuleCreate(BaseModel):
    title: str
    description: str
    sequence_number: int

class ModuleUpdate(BaseModel):
    title: str
    description: str
    sequence_number: int

class OutputModulePage(BasePage):
    data: List[Module]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }