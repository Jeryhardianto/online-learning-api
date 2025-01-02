from pydantic import BaseModel
from datetime import datetime
from enums.enum_tipe import IsDone
from schemas.common_shcema import BasePage
from models.model_todo import Todo
from typing import List

from utils.util_date_time import convert_datetime_str

class Todo(BaseModel):
    title: str
    description: str
    status: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title: str
    description: str
    status: IsDone 

class TodoUpdate(BaseModel):
    title: str
    description: str
    status: IsDone

class TodoIsDone(BaseModel):
    status: IsDone


class OutputTransactionPage(BasePage):
    data: List[Todo]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }