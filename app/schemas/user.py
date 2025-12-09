from pydantic import BaseModel, EmailStr
from typing import Literal


class UserCreate(BaseModel):
    """Schema for user registration."""
    name: str
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str  # Can be username or email
    password: str


class UserResponse(BaseModel):
    """Schema for user response (no password)."""
    id: str
    name: str
    email: str
    username: str
    role: Literal["admin", "user"]


class LoginResponse(BaseModel):
    """Schema for login response."""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
