from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.fee import Fee
from app.models.user import User
from app.schemas.fee import FeeCreate, FeeUpdate, FeeResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/fees", tags=["Fees"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=FeeResponse, status_code=201)
def create_fee(fee: FeeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_fee = Fee(
        amount=fee.amount,
        fee_type=fee.fee_type,
        due_date=fee.due_date,
        student_id=fee.student_id
    )
    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)
    return new_fee

@router.get("/student/{student_id}", response_model=list[FeeResponse])
def get_student_fees(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Fee).filter(Fee.student_id == student_id).all()

@router.put("/{fee_id}", response_model=FeeResponse)
def update_fee(fee_id: int, update: FeeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fee = db.query(Fee).filter(Fee.id == fee_id).first()
    if not fee:
        raise HTTPException(status_code=404, detail="Fee not found")
    if update.status is not None:
        fee.status = update.status
    if update.amount is not None:
        fee.amount = update.amount
    db.commit()
    db.refresh(fee)
    return fee