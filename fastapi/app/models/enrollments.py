from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, default=0.0)
    
    student_id = Column(Integer, ForeignKey("auth_users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("AuthUser", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")