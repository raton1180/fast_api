from fastapi import FastAPI,Depends
from app.config.db import SessionLocal,engine
from app.controllers import user_controller
from app.models import user
from typing import List,Annotated
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request


# Create tables
app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail,
        },
    )
user.Base.metadata.create_all(bind=engine)

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close

db_dependency = Annotated[Session, Depends(get_db)]

# Include routers
app.include_router(user_controller.router)
