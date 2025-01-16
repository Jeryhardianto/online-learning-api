from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.enroll_schema import EnrollComplate, EnrollCreate
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from models.model_module import Module as ModuleModel
from schemas.module_schema import ModuleCreate, ModuleUpdate

class RepositoryModule:
  def __init__(self, session: Session):
        self.session = session

  def get_all(self, page: int, size: int, course_id: int):
    return self.session.query(ModuleModel).filter(ModuleModel.course_id == course_id).order_by(ModuleModel.sequence_number.asc()).offset(page * size).limit(size).all()
  
  def get_by_id(self, id: int):
        return self.session.query(ModuleModel).filter(ModuleModel.id == id).first()

  def get_by_id_course_id(self, id: int, course_id: int):
        return self.session.query(ModuleModel).filter(ModuleModel.course_id == course_id, ModuleModel.id == id).first()
  
  def count(self, course_id: int):
      return self.session.query(ModuleModel).filter(ModuleModel.course_id == course_id).count()
  
  def store_module(self, data: ModuleCreate, course_id: int):
      module = ModuleModel(
          course_id=course_id,
          title=data.title,
          description=data.description,
          sequence_number=data.sequence_number,
          created_at=datetime.now(),
          updated_at=datetime.now()
      )
      self.session.add(module)
      self.session.commit()
      self.session.refresh(module)
      return module
  
  def update(self,id: int, course_id: int, data: ModuleUpdate ):
      module = self.get_by_id_courseId(id, course_id)
      module.title = data.title
      module.description = data.description
      module.sequence_number = data.sequence_number
      module.updated_at = datetime.now()
      self.session.commit()
      self.session.refresh(module)
      return module
  
  def delete(self, id: int, course_id: int):
      module = self.get_by_id_courseId(id, course_id)
      self.session.delete(module)
      self.session.commit()
      return module