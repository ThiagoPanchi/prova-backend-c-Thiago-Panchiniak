from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token
from app.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    if credentials.username != "admin" or credentials.password != "senha":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return TokenResponse(
        access_token=create_access_token(subject=credentials.username),
        token_type="bearer",
    )
