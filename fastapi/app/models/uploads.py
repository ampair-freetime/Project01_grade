from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

#สำหรับ อาจารย์ในการ create update delete  
class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    #file infomation
    file_name = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    #connection with teacher and courses
    teacher_id = Column(Integer,ForeignKey("teachers.id"))
    teacher = relationship("Teacher",back_populates="uploads")
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="uploads")