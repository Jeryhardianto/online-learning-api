from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from models.model_instructors import Instructor as InstructorModel

class RepositoryInstructor:
  def __init__(self, session: Session):
        self.session = session
    
  def get_all(self, skip: int, size: int):
        return self.session.query(InstructorModel).offset(skip).limit(size).all()
    
  def count(self):
      return self.session.query(InstructorModel).count()

  def  get_by_id(self, id: int):
    return self.session.query(InstructorModel).filter(InstructorModel.id == id).first()
  
  def get_by_email(self, email: str):
      return self.session.query(InstructorModel).filter(InstructorModel.email == email).first()

  def store_instructor(self, data: InsructorCreate):
      course = InstructorModel(
          first_name=data.first_name,
          last_name=data.last_name,
          email=data.email,
          bio=data.bio,
          created_at=datetime.now(),
          updated_at=datetime.now()
      )
      self.session.add(course)
      self.session.commit()
      self.session.refresh(course)
      return course
  
  def update(self, id: int, data: InsructorUpdate):
      instructor = self.get_by_id(id)
      instructor.first_name = data.first_name
      instructor.last_name = data.last_name
      instructor.email = data.email
      instructor.bio = data.bio
      instructor.updated_at = datetime.now()
      self.session.commit()
      return instructor
  
  def delete(self, id: int):    
    instructor = self.get_by_id(id)
    self.session.delete(instructor)
    self.session.commit()
    return instructor
  