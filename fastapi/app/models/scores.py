from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean, DateTime, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import UniqueConstraint
from app.db import Base

class Score(Base, SerializerMixin):
    __tablename__ = "scores"
    __table_args__ = (
        UniqueConstraint("student_id", "quiz_id", name="unique_student_quiz"),
    )

    score_id = Column(Integer, primary_key=True, index=True)
    # คะแนนของนักเรียน
    score = Column(Float, default=0.0)
    # เปิดดูแล้วหรือยัง
    unread_flag = Column(Boolean, default=True)
    # section
    section = Column(VARCHAR(50))

    # เชื่อมต่อกับ quiz
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))
    quiz = relationship("Quiz", back_populates="scores")

    student_id = Column(Integer, ForeignKey("students.student_id"))
    student = relationship("Student", back_populates="scores")

    # create/update
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

