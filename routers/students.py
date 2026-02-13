from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Student

router = APIRouter(prefix="/students", tags=["Students"])

####### get api ###########

@router.get("/")
def get_student(db: Session = Depends(get_db)):
    return db.query(Student).all()

####### Post api ###########

@router.post("/")
def create_student(
        name: str,
        Roll_number: int,
        Class: str,
        subject: str,
        db: Session = Depends(get_db)
):
    subject_string = "{" + subject + "}"

    student = Student(
        name=name,
        Roll_number=Roll_number,
        Class=Class,
        subject=subject_string
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student

####### delete api ###########

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        return {"msg": "not found"}

    db.delete(student)
    db.commit()

    return {"msg": "deleted"}


####### put api ###########
@router.put("/{student_id}")
def update_student(
        student_id: int,
        name: str,
        Roll_number: int,
        class_name: str,
        subject: str,
        db: Session = Depends(get_db)
):
    # 1️⃣ find student
    student = db.query(Student).filter(Student.id == student_id).first()

    # 2️⃣ not found
    if not student:
        return {"msg": "student not found"}

    # 3️⃣ update values
    student.name = name
    student.Roll_number = Roll_number
    student.class_name = class_name
    student.subject = "{" + subject + "}"

    # 4️⃣ save
    db.commit()
    db.refresh(student)

    return student
