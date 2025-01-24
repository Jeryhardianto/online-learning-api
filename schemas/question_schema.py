from pydantic import BaseModel
from datetime import datetime
from schemas.common_shcema import BasePage
from typing import List

from utils.util_date_time import convert_datetime_str

class Question(BaseModel):
    id: int
    quiz_id: int
    question: str
    point: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    question: str
    point: int

class QuestionUpdate(BaseModel):
    question: str
    point: int

class OutputQuestionPage(BasePage):
    data: List[Question]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }