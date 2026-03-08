from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from sqlalchemy import Boolean
from datetime import datetime

#สำหรับ อาจารย์ในการ create update delete  
class Upload(Base):
    __tablename__ = "uploads"

    upload_id = Column(VARCHAR, primary_key=True, index=True,server_default=text("gen_random_uuid()"))
    #file infomation
    file_name = Column(VARCHAR(255), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    # update/create/delete
    created_at = Column(DateTime, default=datetime.utcnow)

    #connection with teacher and courses
    teacher_id = Column(VARCHAR, ForeignKey("teachers.teacher_id"))
    teacher = relationship("Teacher",back_populates="uploads")
    course_code = Column(Integer, ForeignKey("courses.course_code"))
    course = relationship("Course", back_populates="uploads")