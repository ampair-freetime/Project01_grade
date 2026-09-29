from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
from app.db import Base

class Enrollment(Base, SerializerMixin):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "course_code", name="unique_student_course"),
        CheckConstraint("status IN ('active', 'dropped')", name="enrollment_status_check"),
        CheckConstraint("joined_via IN ('code', 'csv')", name="enrollment_joined_via_check"),
    )

    enrollment_id = Column(VARCHAR, primary_key=True, index=True, server_default=text("gen_random_uuid()"))

    student_id = Column(VARCHAR, ForeignKey("students.student_id"), nullable=False)
    student = relationship("Student", back_populates="enrollments")

    # course_code = PK ของ courses (int) ไม่ใช่รหัสวิชาแบบ CS212 (นั่นคือ course_id)
    course_code = Column(Integer, ForeignKey("courses.course_code"), nullable=False)
    course = relationship("Course", back_populates="enrollments")

    section = Column(VARCHAR(50))
    # active / dropped
    status = Column(VARCHAR(20), nullable=False, server_default="active")
    # code = join ด้วย join code เอง, csv = มาจากอาจารย์อัปโหลดคะแนน
    joined_via = Column(VARCHAR(20), nullable=False, server_default="code")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
