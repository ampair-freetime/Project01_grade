from pydantic import BaseModel
from typing import Optional

class Teacher_Course(BaseModel):
    course_name: str
    #sec: str

class T_Assignment(BaseModel):
    course_id:int
    quiz_name:str
    full_mark:int