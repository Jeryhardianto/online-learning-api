from pydantic import BaseModel
from datetime import datetime
from schemas.common_shcema import BasePage
from typing import List

from utils.util_date_time import convert_datetime_str

class Insructor(BaseModel):
    first_name: str
    last_name: str
    email: str
    bio: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class InsructorCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    bio: str

class InsructorUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    bio: str

class OutputInsructorPage(BasePage):
    data: List[Insructor]
    
    class Config:
       json_encoders = {
           datetime: convert_datetime_str
       }