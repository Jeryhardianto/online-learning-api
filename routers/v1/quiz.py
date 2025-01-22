from datetime import datetime
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from schemas.common_shcema import TokenData
from schemas.lesson_schema import LessonCreate, LessonUpdate
from schemas.quiz_schema import QuizCreate, QuizUpdate
from services.service_common import get_current_user
from sqlalchemy.orm import Session
from services.service_quiz import ServiceQuiz
from services.service_module import ServiceModule


router = APIRouter(prefix="/quiz", tags=["Quizzes"])

@router.get("/{module_id}/quiz")
async def get_quiz(
   module_id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   page: int = 0,  
   size: int = 10,
   session: Session = Depends(get_db)
):
  service_quiz = ServiceQuiz(session)
  return service_quiz.get_all(page, size, module_id)

@router.post("/{module_id}")
async def insert_quiz(
   module_id: int,
   input_quiz: QuizCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_quiz = ServiceQuiz(session)
  return service_quiz.insert(input_quiz, module_id)

@router.put("/{id}/module/{module_id}")
async def update_quiz(
   id: int,
   module_id: int,
   input_quiz: QuizUpdate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_quiz = ServiceQuiz(session)
  return service_quiz.update(input_quiz, module_id, id)

@router.delete("/{id}/module/{module_id}")
async def delete_quiz(
   id: int,
   module_id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_quiz = ServiceQuiz(session)
  return service_quiz.delete(id, module_id)
