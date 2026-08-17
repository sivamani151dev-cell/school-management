from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roll_number = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    parent_phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", backref="students")
    attendance_records = relationship("Attendance", backref="student")
    grades = relationship("Grade", backref="student")
    fees = relationship("Fee", backref="student")