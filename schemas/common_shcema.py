from pydantic import BaseModel


class StandardResponse(BaseModel):
    detail: str

class Response(BaseModel):
    success: bool
    message: str
    data: dict

class TokenData(BaseModel):
    id: str
    fullname: str

class BasePage(BaseModel):
    page: int
    size: int
    total_data: int
    total_page: int