from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/")
def create_user(name: str, email: str, Mobile_number:str, db: Session = Depends(get_db)):
    user = User(name=name, email=email,Mobile_number=Mobile_number)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"msg": "not found"}

    db.delete(user)
    db.commit()
    return {"msg": "deleted"}


####### put api ###########
@router.put("/{users_id}")
def update_user(
        users_id: int,
        name: str,
        email: str,
        Mobile_number: str,
        db: Session = Depends(get_db)
):

    users = db.query(User).filter(User.id == users_id).first()

    if not users:
        return {"msg": "users not found"}

    users.name = name
    users.email = email
    users.Mobile_number = Mobile_number

    db.commit()
    db.refresh(users)

    return users
