from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
import uuid

from ..schemas.user import UserCreate, UserLogin, UserResponse, LoginResponse
from ..core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user_id,
)
from ..core.config import settings
from ..infrastructure.database import db
from ..domain.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT token.
    """
    user = db.get_user_by_username(credentials.username)
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return LoginResponse(
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            username=user.username,
            role=user.role
        ),
        access_token=access_token
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user.
    """
    # Check if username or email already exists
    existing = db.get_user_by_username(user_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    
    existing_email = db.get_user_by_username(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Create new user
    new_user = User(
        id=str(uuid.uuid4()),
        name=user_data.name,
        email=user_data.email,
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        role="user"
    )
    
    db.create_user(new_user)
    
    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        username=new_user.username,
        role=new_user.role
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    """
    Get current authenticated user.
    """
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        username=user.username,
        role=user.role
    )
