from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.todo_schema import TodoCreate, TodoIsDone, TodoUpdate
from models.model_course import Course as CourseModel

class RepositoryCourse:
  def __init__(self, session: Session):
        self.session = session
    
  def get_all(self, skip: int, size: int):
        return self.session.query(CourseModel).offset(skip).limit(size).all()
    

  def count(self):
      return self.session.query(CourseModel).count()

  def  get_by_id(self, id: int):
    return self.session.query(CourseModel).filter(CourseModel.id == id).first()
  
  # def store_todo(self, data: TodoCreate):
  #     todo = CourseModel(
  #         title        = data.title,
  #         description  = data.description,
  #         status       = data.status,
  #         user_id     = data.user_id,
  #         created_at   = data.created_at,
  #         updated_at   = data.updated_at
  #     )
  #     self.session.add(todo)
  #     self.session.commit()
  #     self.session.refresh(todo)
  #     return todo
  
  # def update(self, id: int, data: TodoUpdate, user_id: int):
  #     todo = self.get_by_id(id, user_id)
  #     todo.title = data.title
  #     todo.description = data.description
  #     todo.status = data.status
  #     todo.updated_at = datetime.now()
  #     self.session.commit()
  #     return todo
  
  # def delete(self, id: int, user_id: int):    
  #   todo = self.get_by_id(id, user_id)
  #   self.session.delete(todo)
  #   self.session.commit()
  #   return todo
  