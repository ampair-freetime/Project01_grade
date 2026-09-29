from pydantic import BaseModel

class EnrollRequest(BaseModel):
    code: str
