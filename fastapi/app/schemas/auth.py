from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    avatar_url: Optional[str] = None
    student_id: Optional[int] = None  # รหัสนักศึกษา
    google_connected: bool

    class Config:
        from_attributes = True

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