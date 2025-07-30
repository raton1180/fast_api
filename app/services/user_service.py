from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_view import UserCreate, UsersResponse,UserData,LoginResponseData,LoginResponse
from app.utils.hash import hash_password, verify_password,create_access_token,decode_access_token
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

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
def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials."
        )
    
    # Remove sensitive field
    user.hashed_password = None  
    
    # Generate token
    access_token = create_access_token(data={"sub": str(user.email)})

    return LoginResponse(
        status=200,
        message="Success",
        data=UserData.from_orm(user),
        access_token=access_token
    )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
   
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
   
    return payload["sub"]
