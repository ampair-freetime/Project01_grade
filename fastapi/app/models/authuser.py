from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from app.db import Base

class AuthUser(Base):
    __tablename__ = "auth_users"

    # ลำดับ id
    auth_user_id = Column(VARCHAR, primary_key=True, index=True)
    email = Column(VARCHAR(100), unique=True, nullable=False)
    password = Column(VARCHAR(255))

    student = relationship("Student", back_populates="auth_user", uselist=False)
    teacher = relationship("Teacher", back_populates="auth_user", uselist=False)
    providers = relationship("AuthProvider", back_populates="auth_user")