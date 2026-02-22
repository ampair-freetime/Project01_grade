from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db import Base

class AuthUser(Base):
    __tablename__ = "auth_users"

    # ลำดับ id
    id = Column(Integer, primary_key=True, index=True)
    # email (ไม่ซ้ำกัน/ไม่เป็นค่าว่าง)
    email = Column(String(100), unique=True, nullable=False)
    # รหัสผ่าน 
    password = Column(String(255), nullable=True)

    student = relationship("Student", back_populates="auth_user")
    teacher = relationship("Teacher", back_populates="auth_user")