from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    Mobile_number = Column(String)

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
    Roll_number = Column(Integer)
    Class = Column(String)
    subject = Column(String)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(String)
    endpoint = Column(String)
    method = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
