from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from enums.enum_tipe import DifficultyLevel

from config.config import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)
    instructor_id  = Column(Integer, ForeignKey("instructors.id"), nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    difiiculty = Column(Enum(DifficultyLevel), nullable=True)
    is_published = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    instructor = relationship('Instructor', back_populates='courses')