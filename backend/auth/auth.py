from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import User
from models.refresh_token import RefreshToken
from datetime import timedelta
from schemas.user import UserCreate
from utils.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_refresh_token,
)
from core.config import settings
import logging


logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserCreate) -> User:
        # Check if email already exists
        logger.info("Registering user: ", user_data.username)
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.error("User already exists")
            raise ValueError("Email already registered")

        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hash_password(user_data.password),
            role=user_data.role
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info("User Registered")
        return user


    @staticmethod
    async def login_user(db: AsyncSession, email: str, password: str):
        logger.info("Logging user in...")
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.error("Invalid creds")
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            logger.error("Invalid creds")
            raise ValueError("Invalid credentials")

        access_token = create_access_token(user.id, user.role)
        refresh_token = create_refresh_token(user.id)

        # Store hashed refresh token
        token_entry = RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=datetime.utcnow()
            + settings.REFRESH_TOKEN_EXPIRE_DAYS * timedelta(days=1),
        )

        db.add(token_entry)
        await db.commit()
        logger.info("Log in successful")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


    @staticmethod
    async def refresh_tokens(db: AsyncSession, refresh_token: str):
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            logger.error("invalid token type")
            raise ValueError("Invalid token type")

        hashed_token = hash_refresh_token(refresh_token)

        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == hashed_token,
                RefreshToken.revoked == False
            )
        )

        token_entry = result.scalar_one_or_none()

        if not token_entry:
            logger.error("Invalid refresh token")
            raise ValueError("Invalid refresh token")

        if token_entry.expires_at < datetime.utcnow():
            logger.error("Refresh token expired")
            raise ValueError("Refresh token expired")

        # Rotate token
        token_entry.revoked = True

        new_access = create_access_token(payload["sub"], payload.get("role", "USER"))
        new_refresh = create_refresh_token(payload["sub"])

        new_token_entry = RefreshToken(
            user_id=payload["sub"],
            token_hash=hash_refresh_token(new_refresh),
            expires_at=datetime.utcnow()
            + settings.REFRESH_TOKEN_EXPIRE_DAYS * timedelta(days=1),
        )

        db.add(new_token_entry)
        await db.commit()
        logger.info("Token refreshed")
        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }

    @staticmethod
    async def logout_user(db: AsyncSession, refresh_token: str):
        hashed = hash_refresh_token(refresh_token)

        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == hashed
            )
        )

        token_entry = result.scalar_one_or_none()

        if token_entry:
            token_entry.revoked = True
            await db.commit()
            logger.info("user logged out")
