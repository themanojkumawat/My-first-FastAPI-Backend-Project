from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Student, Log
from auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    total_users = db.query(User).count()
    total_students = db.query(Student).count()
    total_logs = db.query(Log).count()

    return {
        "status": True,
        "total_users": total_users,
        "total_students": total_students,
        "total_logs": total_logs
    }
