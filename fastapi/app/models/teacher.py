# fastapi/app/models/teacher.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from .authuser import AuthUser

class Teacher(Base) :
    __tablename__ = "teachers"

    # ลำดับ id
    id = Column(Integer, primary_key=True, index=True)
    # ชื่อ/ชื่อกลาง/นามสกุล
    firstname = Column(String(255))
    middlename = Column(String(255))
    lastname = Column(String(255))
    # รูปโปรไฟล์
    avatar_url = Column(String(500))

    # เชื่อมต่อกับ id
    auth_user_id = Column(Integer, ForeignKey("auth_users.id"))
    # เชื่อมต่อกับ login AuthUser
    auth_user = relationship("AuthUser", back_populates="teacher")
    # เชื่อมต่อกับ courses
    courses = relationship("Course", back_populates="teacher")