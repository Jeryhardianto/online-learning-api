from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from config.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(255))
    email = Column(String(255), unique=True, index=True) 
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    todos = relationship("Todo", back_populates="users")
    enrollments = relationship('Enrollment', back_populates='user')