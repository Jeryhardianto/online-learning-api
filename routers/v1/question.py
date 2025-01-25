from datetime import datetime
from typing import List
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from config.config import get_db
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from schemas.common_shcema import TokenData
from schemas.lesson_schema import LessonCreate, LessonUpdate
from schemas.question_schema import AnswerCreate, QuestionCreate, QuestionUpdate
from schemas.quiz_schema import QuizCreate, QuizUpdate
from services.service_common import get_current_user
from sqlalchemy.orm import Session
from services.service_question import ServiceQuestion
from services.service_quiz import ServiceQuiz
from services.service_module import ServiceModule


router = APIRouter(prefix="/question", tags=["Questions"])

@router.get("/{quiz_id}/quiz")
async def get_question(
   quiz_id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   page: int = 0,  
   size: int = 10,
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.get_all(page, size, quiz_id)

@router.post("/{quiz_id}")
async def insert_question(
   quiz_id: int,
   input_question: QuestionCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.insert(input_question, quiz_id)

@router.put("/{id}")
async def update_question(
   id: int,
   input_question: QuestionUpdate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.update(input_question, id)

@router.delete("/{id}")
async def delete_question(
   id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.delete(id)

@router.post("/{question_id}/answer")
async def insert_answer(
   question_id: int,
   input_answer: AnswerCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.insert_answer(input_answer, question_id)

@router.put("/{answer_id}/answer")
async def update_answer(
   answer_id: int,
   input_answer: AnswerCreate,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.update_answer(input_answer, answer_id)
@router.delete("/{answer_id}/answer")
async def delete_answer(
   answer_id: int,
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.delete_answer(answer_id)
# insert batch answer
@router.post("/{question_id}/answers")
async def insert_batch_answer(
   question_id: int,
   input_answer: List[AnswerCreate],
   current_user: Annotated[TokenData, Depends(get_current_user)],
   session: Session = Depends(get_db)
):
  service_question = ServiceQuestion(session)
  return service_question.insert_batch_answer(input_answer, question_id)