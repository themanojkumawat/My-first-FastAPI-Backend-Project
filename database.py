from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ PostgreSQL URL
DATABASE_URL = "postgresql://drivergo:drivergopass@127.0.0.1:5432/drivergo_db"

# ✅ engine
engine = create_engine(DATABASE_URL)

# ✅ session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ base
Base = declarative_base()


# ✅ dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
