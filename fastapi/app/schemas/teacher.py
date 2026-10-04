from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class Teacher_Course(BaseModel):
    course_name: str
    course_id: str
    section: Optional[str] = Field(default=None, max_length=50)

    @field_validator("section", mode="before")
    @classmethod
    def normalize_section(cls, value):
        return value.strip() or None if isinstance(value, str) else value

class Assignment(BaseModel):
    course_code:int
    quiz_name:str
    full_mark:int
    weight:float

class CourseUpdate(Teacher_Course):
    pass

class AssignmentUpdate(BaseModel):
    quiz_name: str
    full_mark: int
    weight: float
