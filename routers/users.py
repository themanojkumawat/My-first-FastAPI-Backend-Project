from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, LoginSchema
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Auth"])


######## REGISTER ########
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        mobile_number=""
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status": True, "message": "User created successfully"}


######## LOGIN ########
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "status": True,
        "token": token,
        "message": "Login successful"
    }


######## GET USERS ########
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
