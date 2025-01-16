from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from config.config import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    sequence_number = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    course = relationship('Course', back_populates='modules')
    lessons = relationship('Lesson', back_populates='module')