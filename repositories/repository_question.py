from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.enroll_schema import EnrollComplate, EnrollCreate
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from schemas.lesson_schema import LessonCreate, LessonUpdate
from schemas.module_schema import ModuleCreate, ModuleUpdate
from schemas.question_schema import AnswerCreate, QuestionCreate, QuestionUpdate
from schemas.quiz_schema import QuizCreate, QuizUpdate
from models.model_question import Question as QuestionModel
from models.model_answer import Answer as AnswerModel


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
  def get_answer_by_id(self, id: int):
      return self.session.query(AnswerModel).filter(AnswerModel.id == id).first()
  
  def store_answer(self, data: AnswerCreate, question_id: int):
      answer = AnswerModel(
        question_id=question_id,
        option_text=data.option_text,
        is_correct=data.is_correct,
        created_at=datetime.now(),
        updated_at=datetime.now()
      )
      self.session.add(answer)
      self.session.commit()
      self.session.refresh(answer)
      return answer 
  def update_answer(self, data: AnswerCreate, id: int):
      answer = self.get_answer_by_id(id)
      answer.option_text = data.option_text
      answer.is_correct = data.is_correct
      answer.updated_at = datetime.now()
      self.session.commit()
      return answer
  def delete_answer(self, id: int):
        answer = self.get_answer_by_id(id)
        self.session.delete(answer)
        self.session.commit()
        return answer
  #   insert batch answer
  def store_answers(self, data: List[AnswerCreate], question_id: int):
      answers = []
      for answer in data:
          answer = AnswerModel(
              question_id=question_id,
              option_text=answer.option_text,
              is_correct=answer.is_correct,
              created_at=datetime.now(),
              updated_at=datetime.now()
          )
          self.session.add(answer)
          self.session.commit()
          self.session.refresh(answer)
          answers.append(answer)
      return answers