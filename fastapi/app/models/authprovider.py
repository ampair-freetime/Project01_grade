from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, text
from sqlalchemy.orm import relationship
from app.db import Base


class AuthProvider(Base):
    __tablename__ = "auth_providers"

    provider_id = Column(VARCHAR, primary_key=True, index=True,server_default=text("gen_random_uuid()"))
    auth_user_id = Column(VARCHAR, ForeignKey("auth_users.auth_user_id"))

    # login provider เช่น google / password
    provider = Column(VARCHAR(50))
    # id จาก provider เช่น google user id
    provider_user_id = Column(VARCHAR(255))

    # เชื่อมกับ auth_user
    auth_user = relationship("AuthUser", back_populates="providers")