from pydantic import BaseModel
from datetime import datetime
from schemas.common_shcema import BasePage
from typing import List

from utils.util_date_time import convert_datetime_str

class Lesson(BaseModel):
    id: int
    module_id: int
    title: str
    content: str
    video_url: str
    duration_minutes: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class LessonCreate(BaseModel):
    title: str
    content: str
    video_url: str
    duration_minutes: int

class LessonUpdate(BaseModel):
    title: str
    content: str
    video_url: str
    duration_minutes: int

class OutputLessonPage(BasePage):
    data: List[Lesson]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }