from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from app.db import Base
from sqlalchemy import Boolean

class Enrollment(Base):
    __tablename__ = "enrollments"
    # ไม่ลงทะเบียนวิชาซ้ำ
    __table_args__ = (
    UniqueConstraint("student_id", "course_id", name="unique_enrollment"),
)

    id = Column(Integer, primary_key=True, index=True) # ลำดับ
    score = Column(Float, default=0.0) # คะแนน (ทศนิยม)
    
    # รหัสนักศึกษา
    student_id = Column(Integer, ForeignKey("students.id"))
    # รายวิชา
    course_id = Column(Integer, ForeignKey("courses.id"))
    # เกรด
    grade = Column(String(2), nullable=True)
    # เช็คว่าอ่านแล้วหรือยัง
    unread_flag = Column(Boolean, default=True)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

