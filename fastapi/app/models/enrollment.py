from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)

    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)

    # Timestamp
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    # student ลงวิชาเดิมซ้ำไม่ได้
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

    # Relationships
    student = relationship("Student", back_populates="enrollments")

    course = relationship("Course", back_populates="enrollments")