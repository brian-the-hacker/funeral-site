import secrets
import time

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import settings

bearer = HTTPBearer(auto_error=False)
TOKEN_HOURS = 12


def check_credentials(username: str, password: str) -> bool:
    if not settings.admin_password or not settings.jwt_secret:
        return False  # refuse to run with an unset password/secret
    ok_user = secrets.compare_digest(username, settings.admin_user)
    ok_pass = secrets.compare_digest(password, settings.admin_password)
    return ok_user and ok_pass


def create_token() -> str:
    payload = {"sub": settings.admin_user, "exp": int(time.time()) + TOKEN_HOURS * 3600}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def require_admin(creds: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if creds is None:
        raise HTTPException(401, "Log in first.")
    try:
        jwt.decode(creds.credentials, settings.jwt_secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(401, "Session expired. Log in again.")
