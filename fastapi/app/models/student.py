# fastapi/app/models/student.py
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from app.db import Base

class Student(Base, SerializerMixin):
    __tablename__ = "students"

    # รหัสนักศึกษา
    student_id = Column(VARCHAR, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    # name
    first_name = Column(VARCHAR(255))
    middle_name = Column(VARCHAR(255))
    last_name = Column(VARCHAR(255))
    # profile
    avatar_url = Column(VARCHAR(500))
    # update/create
    created_at = Column(DateTime, default=datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # เชื่อมต่อกับ id
    auth_user_id = Column(VARCHAR, ForeignKey("auth_users.auth_user_id"))
    auth_user = relationship("AuthUser", back_populates="student")
    # เชื่อมต่อกับ score
    scores = relationship("Score", back_populates="student", cascade="all, delete", passive_deletes=True)