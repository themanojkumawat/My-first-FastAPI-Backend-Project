from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Marks
from auth import get_current_user, admin_required
from schemas import (
    StudentCreate,
    StudentOut,
    StudentWithMarksOut,
    MarksIn,
    MarksOut,
    get_subjects_for_class,
    ALLOWED_CLASSES,
)

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/subjects")
def get_subjects(
    class_name: str = Query(..., description="10th or 12th"),
    current_user: dict = Depends(get_current_user),
):
    """Get fixed subjects for 10th (6) or 12th Biology (5)."""
    if class_name not in ALLOWED_CLASSES:
        raise HTTPException(status_code=400, detail="class_name must be 10th or 12th")
    return {"class_name": class_name, "subjects": get_subjects_for_class(class_name)}


@router.get("/", response_model=list[StudentOut])
def get_students(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    class_name: str | None = Query(None, description="Filter by class: 10th or 12th"),
):
    query = db.query(Student)
    if class_name:
        if class_name not in ALLOWED_CLASSES:
            raise HTTPException(
                status_code=400,
                detail=f"class_name must be one of: {', '.join(ALLOWED_CLASSES)}",
            )
        query = query.filter(Student.class_name == class_name)
    students = query.order_by(Student.roll_number).all()
    return students


@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/{student_id}/marks", response_model=list[MarksOut])
def get_student_marks(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all subject-wise marks for a student."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    marks_list = db.query(Marks).filter(Marks.student_id == student_id).all()
    return marks_list


@router.put("/{student_id}/marks")
def set_student_marks(
    student_id: int,
    body: list[MarksIn],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Set/update subject-wise marks. Only allowed subjects for that class are accepted."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    allowed = get_subjects_for_class(student.class_name)
    # Remove existing marks for this student
    db.query(Marks).filter(Marks.student_id == student_id).delete()
    for m in body:
        if m.subject not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid subject '{m.subject}' for {student.class_name}. Allowed: {allowed}",
            )
        db.add(
            Marks(
                student_id=student_id,
                subject=m.subject,
                marks=min(max(0, m.marks), m.max_marks),
                max_marks=m.max_marks,
            )
        )
    db.commit()
    return {"status": True, "message": "Marks updated", "student_id": student_id}


@router.get("/{student_id}/with-marks", response_model=StudentWithMarksOut)
def get_student_with_marks(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get student with all subject-wise marks."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    marks_list = db.query(Marks).filter(Marks.student_id == student_id).all()
    out = StudentWithMarksOut.model_validate(student)
    out.marks = [MarksOut.model_validate(m) for m in marks_list]
    return out


################ CREATE ################
@router.post("/", response_model=StudentOut)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if student.class_name not in ALLOWED_CLASSES:
        raise HTTPException(
            status_code=400,
            detail=f"class_name must be one of: {', '.join(ALLOWED_CLASSES)}",
        )
    new_student = Student(
        name=student.name,
        roll_number=student.roll_number,
        class_name=student.class_name,
        subject=student.subject
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


################ UPDATE ################
@router.put("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.class_name not in ALLOWED_CLASSES:
        raise HTTPException(
            status_code=400,
            detail=f"class_name must be one of: {', '.join(ALLOWED_CLASSES)}",
        )

    db_student.name = student.name
    db_student.roll_number = student.roll_number
    db_student.class_name = student.class_name
    db_student.subject = student.subject

    db.commit()
    db.refresh(db_student)
    return db_student


################ DELETE ################
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required),
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"status": True, "message": "Deleted successfully"}
