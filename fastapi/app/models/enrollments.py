from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Enrollment(Base, SerializerMixin):
    __tablename__ = "enrollments"
    # ไม่ลงทะเบียนวิชาซ้ำ
    __table_args__ = (
    UniqueConstraint("student_id", "course_id", name="unique_enrollment"),
)

    enrollment_id = Column(Integer, primary_key=True, index=True) # ลำดับ
    # รหัสนักศึกษา
    student_id = Column(Integer, ForeignKey("students.student_id"))
    # รายวิชา
    course_id = Column(Integer, ForeignKey("courses.course_id"))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    scores = relationship("Score", back_populates="enrollment")

