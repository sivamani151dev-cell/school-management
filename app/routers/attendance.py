from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/attendance", tags=["Attendance"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=AttendanceResponse, status_code=201)
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == attendance.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    new_attendance = Attendance(
        student_id=attendance.student_id,
        status=attendance.status,
        teacher_id=attendance.teacher_id
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

@router.get("/student/{student_id}", response_model=list[AttendanceResponse])
def get_student_attendance(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Attendance).filter(Attendance.student_id == student_id).all()