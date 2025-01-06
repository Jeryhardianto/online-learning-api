from datetime import datetime, date
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from enums.enum_tipe import EnrollmentStatus

from config.config import Base


class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    enrolled_date = Column(DateTime, nullable=True)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ENROLLED)
    completion_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
