from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.config.db import SessionLocal
from app.services.user_service import login_user
from app.schemas.user_view import LoginResponse
from typing import List

router = APIRouter(prefix="", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/login", response_model=LoginResponse)
def login(email: str, password: str, response: Response, db: Session = Depends(get_db)):
    login_result = login_user(db, email, password)

    # Set token as HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=login_result.access_token,
        httponly=True,
        secure=False,  # change to True if using HTTPS
        samesite="Lax"
    )

    return login_result
