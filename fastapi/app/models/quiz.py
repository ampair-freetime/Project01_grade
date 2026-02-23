from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Quiz(Base, SerializerMixin):
    __tablename__ = "quizzes"

    quiz_id = Column(Integer, primary_key=True, index=True)
    # เข้าถึงรายวิชา
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    # ชื่อควิซ
    quiz_name = Column(String(255))
    # คะแนนสูงสุด
    full_mark = Column(Integer, default=100)

    # update/create/delete
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    #เชื่อมกับ course
    course = relationship("Course", back_populates="quizzes")
    #เชื่อมกับ scores
    scores = relationship("Score", back_populates="quiz")
