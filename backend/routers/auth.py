from fastapi import APIRouter, HTTPException

import auth
from schemas import LoginIn, TokenOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn):
    if not auth.check_credentials(data.username, data.password):
        raise HTTPException(401, "Wrong username or password.")
    return TokenOut(access_token=auth.create_token())
