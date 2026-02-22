# fastapi/app/models/teacher.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy_serializer import SerializerMixin

class Teacher(Base, SerializerMixin) :
    __tablename__ = "teachers"

    
    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(255))
    middle_name = Column(String(255))
    last_name = Column(String(255))

    avatar_url = Column(String(500))

    #เชื่อมต่อ auth_user
    auth_user_id = Column(Integer, ForeignKey("auth_users.id"))
    auth_user = relationship("AuthUser", back_populates="teacher")
    # เชื่อมต่อกับ courses
    courses = relationship("Course", back_populates="teacher")
    uploads = relationship("Upload", back_populates="teacher")