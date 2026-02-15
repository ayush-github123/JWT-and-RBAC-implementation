from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserResponse
from schemas.auth import TokenPair, LoginRequest, RefreshTokenRequest
from auth.auth import AuthService
from auth.services import get_current_active_user
from models.user import User
from core.database import get_db
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate,db: AsyncSession = Depends(get_db)):
    try:
        user = await AuthService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me")
async def me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/login", response_model=TokenPair)
async def login(credentials: LoginRequest,db: AsyncSession = Depends(get_db)):
    try:
        tokens = await AuthService.login_user(
            db,
            credentials.email,
            credentials.password
        )
        return tokens
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )



@router.post("/refresh", response_model=TokenPair)
async def refresh(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    try:
        tokens = await AuthService.refresh_tokens( db, request.refresh_token )
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )



@router.post("/logout")
async def logout(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    await AuthService.logout_user(db, request.refresh_token)
    return {"message": "Logged out successfully"}


