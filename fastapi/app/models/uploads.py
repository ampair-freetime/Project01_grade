from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy import Boolean
from datetime import datetime

#สำหรับ อาจารย์ในการ create update delete  
class Upload(Base):
    __tablename__ = "uploads"

    upload_id = Column(Integer, primary_key=True, index=True)
    #file infomation
    file_name = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    # update/create/delete
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    #connection with teacher and courses
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"))
    teacher = relationship("Teacher",back_populates="uploads")
    course_id = Column(Integer, ForeignKey("courses.couse_id"))
    course = relationship("Course", back_populates="uploads")