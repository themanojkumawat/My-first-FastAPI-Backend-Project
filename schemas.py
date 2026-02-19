from datetime import datetime
from pydantic import BaseModel

######## USER ########

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True   # ✅ pydantic v2


class LoginSchema(BaseModel):
    email: str
    password: str


######## STUDENT ########

ALLOWED_CLASSES = ["10th", "12th"]

# Fixed subjects: 10th (6) and 12th Biology (5)
SUBJECTS_10TH = ["English", "Math", "Hindi", "Science", "Social Studies", "Sanskrit"]
SUBJECTS_12TH_BIOLOGY = ["Hindi", "English", "Biology", "Chemistry", "Physics"]


def get_subjects_for_class(class_name: str) -> list[str]:
    if class_name == "10th":
        return SUBJECTS_10TH.copy()
    if class_name == "12th":
        return SUBJECTS_12TH_BIOLOGY.copy()
    return []


# 🔥 create/update request
class StudentCreate(BaseModel):
    name: str
    roll_number: int
    class_name: str  # Only "10th" or "12th"
    subject: str = ""  # optional now; use marks for subject-wise numbers


# 🔥 response
class StudentOut(BaseModel):
    id: int
    name: str
    roll_number: int
    class_name: str
    subject: str

    class Config:
        from_attributes = True   # ✅ pydantic v2


######## MARKS ########

class MarksIn(BaseModel):
    subject: str
    marks: int = 0
    max_marks: int = 100


class MarksOut(BaseModel):
    id: int
    student_id: int
    subject: str
    marks: int
    max_marks: int

    class Config:
        from_attributes = True


class StudentWithMarksOut(StudentOut):
    marks: list[MarksOut] = []


######## LOG ########

LOG_LEVELS = ["info", "warning", "error"]


class LogCreate(BaseModel):
    level: str = "info"
    message: str
    endpoint: str = ""
    method: str = ""


class LogOut(BaseModel):
    id: int
    level: str
    message: str
    endpoint: str
    method: str
    status_code: int | None
    user_id: int | None
    ip_address: str | None
    duration_ms: int | None
    created_at: datetime

    class Config:
        from_attributes = True
