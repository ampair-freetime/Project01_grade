from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from app.db import Base

class AuthUser(Base):
    __tablename__ = "auth_users"

    # ลำดับ id
    auth_user_id = Column(Integer, primary_key=True, index=True)
    # email 
    email = Column(VARCHAR, unique=True, nullable=False)
    # รหัสผ่าน 
    password = Column(VARCHAR)

    student = relationship("Student", back_populates="auth_user", uselist=False)
    teacher = relationship("Teacher", back_populates="auth_user", uselist=False)