from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal
from app.services.user_service import create_user, get_users,get_user
from app.schemas.user_view import UserCreate, UsersResponse,UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=UsersResponse)
def list_users(db: Session = Depends(get_db)):
    return get_users(db)
"""  """
@router.get("/{user_id}", response_model=UserResponse)
def get_single_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)
