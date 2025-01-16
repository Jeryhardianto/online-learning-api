from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from config.config import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String(255), index=True)
    content = Column(Text, nullable=True)
    video_url = Column(String(255), nullable=True)
    duration_minutes = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    module = relationship('Module', back_populates='lessons')