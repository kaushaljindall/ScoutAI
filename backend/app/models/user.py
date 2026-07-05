from typing import Optional, List
from datetime import datetime, timezone
from beanie import Indexed
from pydantic import Field, EmailStr
from app.models.base import BaseDocument


class User(BaseDocument):
    email: Indexed(str, unique=True)
    password_hash: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"


class RefreshToken(BaseDocument):
    user_id: str
    token: Indexed(str, unique=True)
    expires_at: datetime
    revoked: bool = False

    class Settings:
        name = "refresh_tokens"


class PasswordResetToken(BaseDocument):
    user_id: str
    token: Indexed(str, unique=True)
    expires_at: datetime
    used: bool = False

    class Settings:
        name = "password_reset_tokens"


class Settings(BaseDocument):
    user_id: Indexed(str, unique=True)
    preferences: dict = {}

    class Settings:
        name = "user_settings"


class AuditLog(BaseDocument):
    user_id: Optional[str] = None
    action: str
    entity: Optional[str] = None
    entity_id: Optional[str] = None
    details: dict = {}

    class Settings:
        name = "audit_logs"
