from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.teacher import Teacher
from app.models.user import User
from app.schemas.teacher import TeacherCreate, TeacherResponse, TeacherUpdate
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/teachers", tags=["Teachers"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=TeacherResponse, status_code=201)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db), current_usr : User = Depends(get_current_user)):
    exisiting = db.query(Teacher).filter(Teacher.email == teacher.email).first()
    if exisiting:
        raise HTTPException(status_code=400, detail="Teacher email already exists")
    new_teacher = Teacher(
        name = teacher.name,
        email = teacher.email,
        phone = teacher.phone,
        subject = teacher.subject,
        experience_years = teacher.experience_years
    )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher

@router.get("/", response_model=list[TeacherResponse])
def get_teachers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Teacher).all()

@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(teacher_id: int, update: TeacherUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if update.name is not None:
        teacher.name = update.name
    if update.phone is not None:
        teacher.phone = update.phone
    if update.subject is not None:
        teacher.subject = update.subject
    if update.is_active is not None:
        teacher.is_active = update.is_active
    db.commit()
    db.refresh(teacher)
    return teacher

@router.delete("/{teacher_id}", status_code=204)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return None