from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.auth.models import Base, User
from backend.auth.schemas import SignupRequest, LoginRequest, TokenResponse
from backend.auth.utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

engine = create_engine("sqlite:///./users.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

@router.post("/signup")
def signup(data: SignupRequest):
    db = SessionLocal()
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}
