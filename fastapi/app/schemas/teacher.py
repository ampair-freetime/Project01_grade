from pydantic import BaseModel
from typing import Optional

class Teacher_Course(BaseModel):
    course_name: str
    course_id: str
    #sec: str

class Assignment(BaseModel):
    course_code:int
    quiz_name:str
    full_mark:int
    weight:float

class CourseUpdate(BaseModel):
    course_name: str
    course_id: str

class AssignmentUpdate(BaseModel):
    quiz_name: str
    full_mark: int
    weight: float