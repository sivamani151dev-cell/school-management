from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.fee import FeeStatus

class FeeCreate(BaseModel):
    amount: float
    fee_type: str
    due_date: Optional[datetime] = None
    student_id: int

class FeeUpdate(BaseModel):
    status: Optional[FeeStatus] = None
    amount: Optional[float] = None

class FeeResonse(BaseModel):
    id: int
    amount: float
    fee_type: str
    status: FeeStatus
    due_date: Optional[datetime]
    created_at: datetime
    student_id: int

    class Config:
        from_attributes = True