from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.grade import Grade
from app.models.user import User
from app.schemas.grade import GradeCreate, GradeResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/grades", tags=["Grades"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=GradeResponse, status_code=201)
def add_grade(grade: GradeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_grade = Grade(
        subject=grade.subject,
        marks=grade.marks,
        max_marks=grade.max_marks,
        exam_type=grade.exam_type,
        student_id=grade.student_id,
        teacher_id=grade.teacher_id
    )
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

@router.get("/student/{student_id}", response_model=list[GradeResponse])
def get_student_grades(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Grade).filter(Grade.student_id == student_id).all()