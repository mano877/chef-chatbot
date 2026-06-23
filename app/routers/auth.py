"""Authentication router: register and login endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(request: RegisterRequest):
    """Register a new user."""
    result = register_user(request.username, request.email, request.password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "User registered successfully", "user": result["user"]}


@router.post("/login")
async def login(request: LoginRequest):
    """Login and get a JWT token."""
    result = authenticate_user(request.username, request.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])
    return {
        "message": "Login successful",
        "token": result["token"],
        "user": result["user"],
    }
