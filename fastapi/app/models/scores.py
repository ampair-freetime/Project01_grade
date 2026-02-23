from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Score(Base):
    __tablename__ = "scores"

    score_id = Column(Integer, primary_key=True, index=True)

    # คะแนนของนักเรียน
    score = Column(Float, default=0.0)
    # เปิดดูแล้วหรือยัง
    unread_flag = Column(Boolean, default=True)

    # เชื่อมต่อกับ enrollment
    enrollment_id = Column(Integer, ForeignKey("enrollments.enrollment_id"))
    enrollment = relationship("Enrollment", back_populates="scores")

    # เชื่อมต่อกับ quiz
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))
    quiz = relationship("Quiz", back_populates="scores")

    # create/update
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

