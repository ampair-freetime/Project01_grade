from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StudentBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    avatar_url: Optional[str] = None

class StudentCreate(StudentBase):
    auth_user_id: int # เช่น id:5 เป็นลำดับ


class StudentResponse(StudentBase):
    student_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # เพื่อให้อ่านค่าจาก SQLAlchemy Model ได้