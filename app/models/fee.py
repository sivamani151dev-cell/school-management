from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class FeeStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    overdue = "overdue"

class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    fee_type = Column(String, nullable=False)
    status = Column(Enum(FeeStatus), default=FeeStatus.pending)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    student_id = Column(Integer, ForeignKey("students.id"))