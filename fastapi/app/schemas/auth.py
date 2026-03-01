from pydantic import BaseModel, EmailStr
from typing import Optional

# ใช้สำหรับการส่งข้อมูล User กลับไปหา Frontend
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None
    role: str              # เพิ่ม: student หรือ teacher
    student_id: Optional[str] = None  # เพิ่ม: รหัสนักศึกษา (ถ้ามี)

    class Config:
        from_attributes = True  # เพื่อให้อ่านค่าจาก SQLAlchemy Model ได้

class Message(BaseModel):
    message: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignin(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    email: EmailStr
    student_id: Optional[int]
    password: str