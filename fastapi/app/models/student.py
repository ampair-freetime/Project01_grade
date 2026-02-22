# fastapi/app/models/student.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from app.db import Base

class Student (Base, SerializerMixin) :
    __tablename__ = "students"


    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, unique=True, nullable=False)
 
    first_name = Column(String(255))
    middle_name = Column(String(255))
    last_name = Column(String(255))

    avatar_url = Column(String(500))

    # เชื่อมต่อกับ id
    auth_user_id = Column(Integer, ForeignKey("auth_users.id"))
    auth_user = relationship("AuthUser", back_populates="student")
    # เชื่อมต่อกับ enrollment
    enrollments = relationship("Enrollment", back_populates="student")