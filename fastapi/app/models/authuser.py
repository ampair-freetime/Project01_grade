# fastapi/app/models/authuser.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum
from app.db import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class AuthUser(Base):
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(1000))
    avatar_url = Column(String(500))
    password = Column(String(255), nullable=True)

    # เพิ่มฟิลด์ใหม่
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    student_id = Column(String(50), unique=True, nullable=True) # เฉพาะนักเรียน

    # Relationships
    # ใช้ String เพื่อเลี่ยงปัญหา Circular Import
    courses = relationship("Course", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")