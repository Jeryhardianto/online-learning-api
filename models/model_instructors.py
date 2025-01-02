from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from enums.enum_tipe import DifficultyLevel

from config.config import Base


class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    courses = relationship('Course', back_populates='instructor')