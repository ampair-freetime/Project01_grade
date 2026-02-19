from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True) # รหัสวิชา เช่น CS101
    name = Column(String(200), nullable=False)
    
    teacher_id = Column(Integer, ForeignKey("auth_users.id"))
    teacher = relationship("AuthUser", back_populates="courses")

    enrollments = relationship("Enrollment", back_populates="course")