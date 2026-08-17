from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/students", tags=["Students"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Student).filter(Student.roll_number == student.roll_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Roll number already exists")
    new_student = Student(
        name = student.name,
        roll_number = student.roll_number,
        age = student.age,
        grade = student.grade,
        phone = student.phone,
        parent_phone = student.parent_phone,
        owner_id = current_user.id
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/", response_model=list[StudentResponse])
def get_student(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="student not found")
    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, update: StudentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if update.name is not None:
        student.name = update.name
    if update.age is not None:
        student.age = update.age
    if update.grade is not None:
        student.grade = update.grade
    if update.phone is not None:
        student.phone = update.phone
    if update.parent_phone is not None:
        student.parent_phone = update.parent_phone
    if update.is_active is not None:
        student.is_active = update.is_active
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None