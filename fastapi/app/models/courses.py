from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)

    course_name = Column(String(255))
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    uploads = relationship("Upload", back_populates="course")
    quizzes = relationship("Quiz", back_populates="course")