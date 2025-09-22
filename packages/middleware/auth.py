from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os

# Authentication middleware
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthMiddleware:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": now  # Add issued at time
        })
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None

    @staticmethod
    async def is_token_blacklisted(db, token: str) -> bool:
        """Check if token is blacklisted"""
        blacklisted_token = await db.blacklisted_tokens.find_one({"token": token})
        return blacklisted_token is not None

    @staticmethod
    async def blacklist_token(db, token: str, user_id: str) -> bool:
        """Add token to blacklist"""
        try:
            # Get token expiration time
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            expires_at = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
            
            from ..types.models import BlacklistedToken
            blacklisted_token = BlacklistedToken(
                token=token,
                user_id=user_id,
                expires_at=expires_at
            )
            
            await db.blacklisted_tokens.insert_one(blacklisted_token.dict())
            return True
        except JWTError:
            return False

    @staticmethod
    async def blacklist_all_user_tokens(db, user_id: str) -> bool:
        """Add all active tokens for a user to blacklist by storing user logout timestamp"""
        try:
            current_time = datetime.now(timezone.utc)
            
            # Store user logout timestamp to invalidate all previous tokens
            await db.user_logout_timestamps.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "logout_timestamp": current_time,
                        "updated_at": current_time
                    }
                },
                upsert=True
            )
            return True
        except Exception:
            return False

    @staticmethod
    async def is_token_valid_after_logout_all(db, token: str, user_id: str) -> bool:
        """Check if token was issued after user's last logout-all-devices action"""
        try:
            # Get token issued time
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_issued_at = datetime.fromtimestamp(payload.get("iat", 0), tz=timezone.utc)
            
            # Get user's last logout-all timestamp
            logout_record = await db.user_logout_timestamps.find_one({"user_id": user_id})
            if logout_record:
                logout_timestamp = logout_record["logout_timestamp"]
                return token_issued_at > logout_timestamp
            
            return True  # No logout-all record means token is valid
        except JWTError:
            return False

    @staticmethod
    async def cleanup_expired_tokens(db):
        """Remove expired blacklisted tokens from database"""
        current_time = datetime.now(timezone.utc)
        await db.blacklisted_tokens.delete_many({"expires_at": {"$lt": current_time}})

    @staticmethod
    async def get_current_user(db, token: str):
        from ..types.models import User
        
        # Check if token is blacklisted
        if await AuthMiddleware.is_token_blacklisted(db, token):
            return None
            
        user_id = AuthMiddleware.verify_token(token)
        if user_id is None:
            return None
        
        # Check if token is valid after logout-all-devices
        if not await AuthMiddleware.is_token_valid_after_logout_all(db, token, user_id):
            return None
        
        user_data = await db.users.find_one({"id": user_id})
        if user_data:
            return User(**user_data)
        return None
