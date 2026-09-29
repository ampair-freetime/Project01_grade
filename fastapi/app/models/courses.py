from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, Boolean, text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from app.db import Base

class Course(Base, SerializerMixin):
    __tablename__ = "courses"

    course_code = Column(Integer, primary_key=True, index=True)

    course_name = Column(VARCHAR(255))
    course_id = Column(VARCHAR)
    # รหัสให้นักศึกษา join เอง (6 ตัว, ไม่มี 0/O/1/I)
    join_code = Column(VARCHAR(8), unique=True, index=True)
    join_open = Column(Boolean, nullable=False, default=True, server_default=text("true"))
    teacher_id = Column(VARCHAR, ForeignKey("teachers.teacher_id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    is_archive = Column(Boolean, default=False)

    teacher = relationship("Teacher", back_populates="courses")
    uploads = relationship("Upload", back_populates="course")
    quizzes = relationship("Quiz",back_populates="course",cascade="all, delete",passive_deletes=True)
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete", passive_deletes=True)