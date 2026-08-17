from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.attendance import AttendanceStatus

class AttendanceCreate(BaseModel):
    student_id: int
    status: AttendanceStatus = AttendanceStatus.present
    teacher_id: Optional[int] = None

class AttendanceResponse(BaseModel):
    id: int
    date: datetime
    status: AttendanceStatus
    student_id: int
    teacher_id: Optional[int]

    class Config:
        from_attributes = True