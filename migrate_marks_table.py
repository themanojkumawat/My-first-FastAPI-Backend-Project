"""
Create marks table. Run once: python migrate_marks_table.py
"""
from database import engine, Base
from models import Marks
import models  # noqa: F401 - register all models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine, tables=[Marks.__table__])
    print("✅ Marks table created.")
