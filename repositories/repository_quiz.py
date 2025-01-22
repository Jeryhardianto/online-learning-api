from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.enroll_schema import EnrollComplate, EnrollCreate
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from models.model_quiz import Quiz as QuizModel
from schemas.lesson_schema import LessonCreate, LessonUpdate
from schemas.module_schema import ModuleCreate, ModuleUpdate
from schemas.quiz_schema import QuizCreate, QuizUpdate


class RepositoryQuiz:
  def __init__(self, session: Session):
        self.session = session

  def get_all(self, page: int, size: int, module_id: int):
      return self.session.query(QuizModel).filter(QuizModel.module_id == module_id).offset(page * size).limit(size).all()
  
  def get_by_id(self, id: int):
      return self.session.query(QuizModel).filter(QuizModel.id == id).first()
  
  def count(self, module_id: int):
      return self.session.query(QuizModel).filter(QuizModel.module_id == module_id).count()
  
  def store(self, data: QuizCreate, module_id: int):
      quiz = QuizModel(
        module_id=module_id,
        title=data.title,
        passing_score=data.passing_score,
        created_at=datetime.now(),
        updated_at=datetime.now()
      )
      self.session.add(quiz)
      self.session.commit()
      self.session.refresh(quiz)
      return quiz
  
  def update(self, data: QuizUpdate, id: int):
      quiz = self.get_by_id(id)
      quiz.title = data.title
      quiz.passing_score = data.passing_score
      quiz.updated_at = datetime.now()
      self.session.commit()
      self.session.refresh(quiz)
      return quiz

  def delete(self, id: int):
      quiz = self.get_by_id(id)
      self.session.delete(quiz)
      self.session.commit()
      return quiz