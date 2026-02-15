from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from jose import JWTError
from models.user import User
from utils.utils import decode_token
from core.database import get_db
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



async def get_current_user( token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db),) -> User:
    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            logger.error("Invalid token type")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")

        if not user_id:
            logger.error("Invalid token payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

    except JWTError:
        logger.error("Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        logger.error("User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    logger.info("Current user fetched...")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user),) -> User:
    if not current_user.is_active:
        logger.error("Inactive user")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user



def require_role(required_role: str):
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role != required_role:
            logger.error("Permission denied")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return role_checker
