from fastapi import FastAPI,Depends
from app.config.db import SessionLocal,engine
from app.controllers import user_controller,auth_controller
from app.models import user
from typing import List,Annotated
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.middleware.token_validator import TokenValidatorMiddleware 
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

# Create tables
app = FastAPI()
security = HTTPBearer()
app.add_middleware(TokenValidatorMiddleware)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



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
app.include_router(auth_controller.router)
