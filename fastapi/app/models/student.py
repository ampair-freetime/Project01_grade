# fastapi/app/models/student.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from app.db import Base

class Student(Base, SerializerMixin):
    __tablename__ = "students"

    # รหัสนักศึกษา
    student_id = Column(Integer, primary_key=True, index=True)
    # name
    first_name = Column(String(255))
    middle_name = Column(String(255))
    last_name = Column(String(255))
    # profile
    avatar_url = Column(String(500))
    # update/create
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # เชื่อมต่อกับ id
    auth_user_id = Column(Integer, ForeignKey("auth_users.auth_user_id"))
    auth_user = relationship("AuthUser", back_populates="student")
    # เชื่อมต่อกับ enrollment
    scores = relationship("Score",back_populates="student")