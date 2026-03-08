from pydantic import BaseModel
from typing import Optional

class Teacher_Course(BaseModel):
    course_name: str
    course_id: str
    #sec: str

class T_Assignment(BaseModel):
    course_code:int
    quiz_name:str
    full_mark:int