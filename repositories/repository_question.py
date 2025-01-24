from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.enroll_schema import EnrollComplate, EnrollCreate
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from schemas.lesson_schema import LessonCreate, LessonUpdate
from schemas.module_schema import ModuleCreate, ModuleUpdate
from schemas.question_schema import QuestionCreate, QuestionUpdate
from schemas.quiz_schema import QuizCreate, QuizUpdate
from models.model_question import Question as QuestionModel


class RepositoryQuestion:
  def __init__(self, session: Session):
        self.session = session

  def get_all(self, page: int, size: int, quiz_id: int):
      return self.session.query(QuestionModel).filter(QuestionModel.quiz_id == quiz_id).offset(page * size).limit(size).all()
  
  def get_by_id(self, id: int):
      return self.session.query(QuestionModel).filter(QuestionModel.id == id).first()
  
  def count(self, quiz_id: int):
      return self.session.query(QuestionModel).filter(QuestionModel.quiz_id == quiz_id).count()
  
  def store(self, data: QuestionCreate, quiz_id: int):
      question = QuestionModel(
        quiz_id=quiz_id,
        question=data.question,
        point=data.point,
        created_at=datetime.now(),
        updated_at=datetime.now()
      )
      self.session.add(question)
      self.session.commit()
      self.session.refresh(question)
      return question
  
  def update(self, data: QuestionUpdate, id: int):
      question = self.get_by_id(id)
      question.question = data.question
      question.point = data.point
      question.updated_at = datetime.now()
      self.session.commit()
      return question

  def delete(self, id: int):
      question = self.get_by_id(id)
      self.session.delete(question)
      self.session.commit()
      return question