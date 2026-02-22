from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from app.db import Base

class Score(Base, SerializerMixin):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)

    score_name = Column(String)
    score_float = Column(Float, default=0.0)
    unread_flag = Column(Boolean, default=False)
    max_score = Column(Float, default=100.0)
    #เชื่อมกับ enrollments
    enrollment_id = Column(Integer,ForeignKey("enrollments.id"))
    enrollment = relationship("Enrollment", back_populates="scores")