from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Log

router = APIRouter(prefix="/logs", tags=["Logs"])


# GET all logs
@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    return db.query(Log).all()


# POST create log
@router.post("/")
def create_log(level: str, message: str, endpoint: str, method: str, db: Session = Depends(get_db)):

    log = Log(
        level=level,
        message=message,
        endpoint=endpoint,
        method=method
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
