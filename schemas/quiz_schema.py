from pydantic import BaseModel
from datetime import datetime
from schemas.common_shcema import BasePage
from typing import List

from utils.util_date_time import convert_datetime_str

class Quiz(BaseModel):
    id: int
    module_id: int
    title: str
    passing_score: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class QuizCreate(BaseModel):
    title: str
    passing_score: int

class QuizUpdate(BaseModel):
    title: str
    passing_score: int

class OutputQuizPage(BasePage):
    data: List[Quiz]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }