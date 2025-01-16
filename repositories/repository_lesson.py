from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.enroll_schema import EnrollComplate, EnrollCreate
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from models.model_lesson import Lesson as LessonModel
from schemas.lesson_schema import LessonCreate, LessonUpdate
from schemas.module_schema import ModuleCreate, ModuleUpdate


class RepositoryLesson:
  def __init__(self, session: Session):
        self.session = session

  def get_all(self, page: int, size: int, module_id: int):
      return self.session.query(LessonModel).filter(LessonModel.module_id == module_id).offset(page * size).limit(size).all()
  
  def get_by_id(self, id: int):
      return self.session.query(LessonModel).filter(LessonModel.id == id).first()

  def get_by_id_module_id(self, id: int, module_id: int):
        return self.session.query(LessonModel).filter(LessonModel.module_id == module_id, LessonModel.id == id).first()
  
  def count(self, module_id: int):
      return self.session.query(LessonModel).filter(LessonModel.module_id == module_id).count()
  
  def store_lesson(self, data: LessonCreate, module_id: int):
      lesson = LessonModel(
        module_id=module_id,
        title=data.title,
        content=data.content,
        video_url=data.video_url,
        duration_minutes=data.duration_minutes,
        created_at=datetime.now(),
        updated_at=datetime.now()
      )
      self.session.add(lesson)
      self.session.commit()
      self.session.refresh(lesson)
      return lesson
  
  def update(self,id: int, module_id: int, data: LessonUpdate ):
      lesson = self.get_by_id_module_id(id, module_id)
      lesson.title = data.title
      lesson.content = data.content
      lesson.video_url = data.video_url
      lesson.duration_minutes = data.duration_minutes
      lesson.updated_at = datetime.now()
      self.session.commit()
      self.session.refresh(lesson)
      return lesson
  
#   def delete(self, id: int, course_id: int):
#       module = self.get_by_id(id, course_id)
#       self.session.delete(module)
#       self.session.commit()
#       return module