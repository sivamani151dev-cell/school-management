from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GradeCreate(BaseModel):
    subject: str
    marks: float
    max_marks: float
    exam_type: str
    student_id: int
    teacher_id: Optional[int] = None

class GradeResponse(BaseModel):
    id: int
    subject: str
    marks: float
    max_marks: float
    exam_type: str
    student_id: int
    teacher_id: Optional[int]

    class Config:
        from_attributes = True