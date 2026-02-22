from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy_serializer import SerializerMixin

class Course(Base, SerializerMixin):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True) # ลำดับ
    course_id = Column(String(20), unique=True, index=True) # รหัสวิชา เช่น CS101
    course_name = Column(String(200), nullable=False) # ชื่อวิชา

    # เชื่อมต่อกับ teacher
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses")

    # เชื่อมต่อกับ enrollment
    enrollments = relationship("Enrollment", back_populates="course")
    uploads = relationship("Upload", back_populates="courses")