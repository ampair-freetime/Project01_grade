from sqlalchemy import Column, Integer, Float, ForeignKey, VARCHAR, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from app.db import Base
from datetime import datetime

class Quiz(Base, SerializerMixin):
    __tablename__ = "quizzes"
    serialize_rules = ("-scores.quiz",)

    quiz_id = Column(VARCHAR, primary_key=True, index=True)
    # เข้าถึงรายวิชา
    course_code = Column(Integer, ForeignKey("courses.course_code"))
    # ชื่อควิซ
    quiz_name = Column(VARCHAR(255))
    # คะแนนสูงสุด
    full_mark = Column(Integer, default=100)
    # น้ำหนักคะแนน 
    weight = Column(Float, default=1.0)
    is_publish = Column(Boolean,default=False)

    # update/create/delete
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    #เชื่อมกับ course
    course = relationship("Course", back_populates="quizzes")
    #เชื่อมกับ scores
    scores = relationship("Score", back_populates="quiz", cascade="all, delete", passive_deletes=True)
