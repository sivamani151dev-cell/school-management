from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    roll_number: str
    age: int
    grade: str
    phone: Optional[str] = None
    parent_phone: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    phone: Optional[str] = None
    parent_phone: Optional[str] = None
    is_active: Optional[bool] = None

class StudentRessonse(BaseModel):
    id: int
    name: str
    age: int
    grade: str
    phone: Optional[str] 
    parent_phone: Optional[str]
    is_active: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True