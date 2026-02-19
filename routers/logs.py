from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Log
from schemas import LogOut, LogCreate, LOG_LEVELS
from auth import get_current_user, admin_required

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/", response_model=list[LogOut])
def get_logs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    level: str | None = Query(None, description="Filter by level: info, warning, error"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    """List logs with optional level filter and pagination. Newest first."""
    query = db.query(Log)
    if level and level in LOG_LEVELS:
        query = query.filter(Log.level == level)
    logs = query.order_by(Log.created_at.desc()).offset(skip).limit(limit).all()
    return logs


@router.get("/count")
def get_logs_count(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    level: str | None = Query(None, description="Filter by level"),
):
    """Total count of logs, optionally filtered by level."""
    query = db.query(Log)
    if level and level in LOG_LEVELS:
        query = query.filter(Log.level == level)
    return {"count": query.count()}


@router.post("/", response_model=LogOut)
def create_log(
    body: LogCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    """Create a custom log entry (admin only). Auto request logs come from middleware."""
    if body.level not in LOG_LEVELS:
        body.level = "info"
    log = Log(
        level=body.level,
        message=body.message,
        endpoint=body.endpoint or "",
        method=body.method or "",
        status_code=None,
        user_id=current_user.get("user_id"),
        ip_address=None,
        duration_ms=None,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
