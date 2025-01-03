from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.course_schema import CourseCreate, CourseUpdate
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
  
  def store_course(self, data: CourseCreate):
      course = CourseModel(
            title=data.title,
            description=data.description,
            instructor_id=data.instructor_id,
            price=data.price,
            difiiculty=data.difiiculty,
            is_published=data.is_published,
            created_at=datetime.now(),
            updated_at=datetime.now()
      )
      self.session.add(course)
      self.session.commit()
      self.session.refresh(course)
      return course
  
  def update(self, id: int, data: CourseUpdate):
      course = self.get_by_id(id)
      course.title = data.title
      course.description = data.description
      course.instructor_id = data.instructor_id
      course.price = data.price
      course.difiiculty = data.difiiculty
      course.is_published = data.is_published
      course.updated_at = datetime.now()
      self.session.commit()
      return course
  
  def upload_image_by_id(self, id: int, image: str):
      course = self.get_by_id(id)
      course.image = str(image)
      self.session.commit()
      return course
  
  def delete(self, id: int):    
    course = self.get_by_id(id)
    self.session.delete(course)
    self.session.commit()
    return course
  