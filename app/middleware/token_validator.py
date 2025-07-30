from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError
from app.utils.hash import decode_access_token 
from starlette.routing import Match

security = HTTPBearer()

class TokenValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        route = request.app.router.routes

        for r in route:
            match, _ = r.matches(request.scope)
            if match == Match.FULL:
                endpoint = getattr(r, "endpoint", None)
                if endpoint and getattr(endpoint, "is_protected", False):
                    # First check Authorization header
                    token = None
                    auth_header = request.headers.get("Authorization")
                    if auth_header and auth_header.startswith("Bearer "):
                        token = auth_header.split(" ")[1]
                    else:
                        # Fallback: read from cookie
                        token = request.cookies.get("access_token")

                    if not token:
                        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

                    try:
                        payload = decode_access_token(token)
                        if not payload:
                            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
                        request.state.user = payload["sub"]
                    except JWTError:
                        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

                break

        return await call_next(request)
