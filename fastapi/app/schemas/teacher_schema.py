from pydantic import BaseModel
from typing import Optional

class Teacher_Course(BaseModel):
    course_id: int
    course_name: str
    #sec: str