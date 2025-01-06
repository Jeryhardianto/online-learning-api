from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from schemas.enroll_schema import EnrollComplate, EnrollCreate
from schemas.instructor_schema import InsructorCreate, InsructorUpdate
from models.model_enroll import Enrollment as EnrollmentModel

class RepositoryEnroll:
  def __init__(self, session: Session):
        self.session = session
    
  def get_all(self, skip: int, size: int, match_filter: dict):
      user_id = EnrollmentModel.user_id == match_filter["user_id"]
      return self.session.query(EnrollmentModel).filter(user_id).offset(skip).limit(size).all()
    
  def count(self, match_filter: dict):
      user_id = EnrollmentModel.user_id == match_filter["user_id"]
      return self.session.query(EnrollmentModel).filter(user_id).count()
  
  def check_course_is_enroll(self, user_id: int, course_id: int):
      user_id = EnrollmentModel.user_id == user_id
      course_id = EnrollmentModel.course_id == course_id
      return self.session.query(EnrollmentModel).filter(user_id, course_id).first()
  
  def store_enroll(self, data: EnrollCreate, user_id: int):
      enroll = EnrollmentModel(
            user_id=user_id,
            course_id=data.course_id,
            enrolled_date=data.enrolled_date,
            status=data.status,
            created_at=datetime.now(),
            updated_at=datetime.now()
      )
      self.session.add(enroll)
      self.session.commit()
      self.session.refresh(enroll)
      return enroll
  
  def update_enroll(self, user_id: int, course_id: int, data: EnrollComplate):
      enroll = self.check_course_is_enroll(user_id, course_id)
      enroll.status = data.status
      enroll.completion_date = data.completion_date
      enroll.updated_at = datetime.now()
      self.session.commit()
  