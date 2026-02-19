from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    mobile_number = Column(String)
    role = Column(String, default="user")


class test(Base):
    __tablename__ = "testing"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    last_name = Column(String)
    Mobile_number = Column(String)



class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    roll_number = Column(Integer, unique=True)
    class_name = Column(String)
    subject = Column(String)  # kept for backward compatibility; use Marks for subject-wise numbers


class Marks(Base):
    """Subject-wise marks for a student (10th: 6 subjects, 12th Biology: 5 subjects)."""
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String, nullable=False)
    marks = Column(Integer, default=0)       # marks obtained
    max_marks = Column(Integer, default=100)  # max marks for the subject


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, default="info")  # info, warning, error
    message = Column(String)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer, nullable=True)   # HTTP status (200, 404, 500)
    user_id = Column(Integer, nullable=True)      # if authenticated
    ip_address = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)  # request duration in ms
    created_at = Column(DateTime, default=datetime.utcnow)

