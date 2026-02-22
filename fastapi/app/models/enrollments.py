from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from app.db import Base
from sqlalchemy import Boolean
from sqlalchemy_serializer import SerializerMixin

class Enrollment(Base, SerializerMixin):
    __tablename__ = "enrollments"
    # ไม่ลงทะเบียนวิชาซ้ำ
    __table_args__ = (
    UniqueConstraint("student_id", "course_id", name="unique_enrollment"),
)

    id = Column(Integer, primary_key=True, index=True) # ลำดับ

    # รหัสนักศึกษา
    student_id = Column(Integer, ForeignKey("students.id"))
    # รายวิชา
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    scores = relationship("Score", back_populates="enrollments")

