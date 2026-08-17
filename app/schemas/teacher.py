from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    experience_years: Optional[int] = None

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    subject: Optional[str] = None
    is_active: Optional[bool] = None

class TeacherResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    subject: str
    experience_years: Optional[int]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 