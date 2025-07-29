from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_view import UserCreate, UsersResponse,UserData
from app.utils.hash import hash_password
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return {
            "status": 200,
            "message": "Success",
            "data": UserData.from_orm(db_user)
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists. Please use a different email."
        )
def get_users(db: Session):
    users = db.query(User).all()
    users_data = [UserData.from_orm(user) for user in users]
    return {
        "status": 200,
        "message": "Success",
        "data": users_data
    }
def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status": 200,
        "message": "Success",
        "data": UserData.from_orm(user)
    }