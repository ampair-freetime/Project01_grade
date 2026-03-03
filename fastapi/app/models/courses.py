from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from app.db import Base

class Course(Base, SerializerMixin):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)

    course_name = Column(VARCHAR(255))
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    teacher = relationship("Teacher", back_populates="courses")
    uploads = relationship("Upload", back_populates="course")
    quizzes = relationship("Quiz",back_populates="course",cascade="all, delete",passive_deletes=True)