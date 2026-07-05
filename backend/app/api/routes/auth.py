import uuid
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import CurrentUser
from app.core import security
from app.core.config import settings
from app.models.user import User, AuditLog, RefreshToken, PasswordResetToken
from app.schemas.user import UserCreate, UserResponse, Token, RefreshTokenRequest, ForgotPassword, ResetPassword, ChangePassword

router = APIRouter()

async def log_audit(action: str, user_id: str = None, entity: str = None, entity_id: str = None, details: dict = None):
    audit = AuditLog(user_id=user_id, action=action, entity=entity, entity_id=entity_id, details=details or {})
    await audit.insert()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate) -> Any:
    existing = await User.find_one(User.email == user_in.email, User.is_deleted == False)
    if existing:
        raise HTTPException(status_code=400, detail="The user with this email already exists.")
    
    user = User(
        email=user_in.email,
        password_hash=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    await user.insert()
    await log_audit("register", user_id=str(user.id), entity="user", entity_id=str(user.id))
    return user

@router.post("/login", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await User.find_one(User.email == form_data.username, User.is_deleted == False)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    user.last_login = datetime.now(timezone.utc)
    await user.save()

    access_token = security.create_access_token(str(user.id))
    refresh_token_str = security.create_refresh_token(str(user.id))

    db_token = RefreshToken(
        user_id=str(user.id),
        token=refresh_token_str,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    await db_token.insert()
    await log_audit("login", user_id=str(user.id), entity="user", entity_id=str(user.id))

    return {"access_token": access_token, "refresh_token": refresh_token_str, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest) -> Any:
    try:
        payload = security.jwt.decode(request.refresh_token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    db_token = await RefreshToken.find_one(RefreshToken.token == request.refresh_token, RefreshToken.revoked == False)
    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired or invalid")

    user = await User.find_one(User.id == user_id, User.is_deleted == False)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found or inactive")

    db_token.revoked = True
    await db_token.save()

    access_token = security.create_access_token(str(user.id))
    new_refresh = security.create_refresh_token(str(user.id))

    new_token = RefreshToken(
        user_id=str(user.id),
        token=new_refresh,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    await new_token.insert()
    await log_audit("token_refresh", user_id=str(user.id), entity="user", entity_id=str(user.id))

    return {"access_token": access_token, "refresh_token": new_refresh, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: CurrentUser) -> Any:
    return current_user

@router.post("/logout")
async def logout(current_user: CurrentUser, request: RefreshTokenRequest) -> Any:
    db_token = await RefreshToken.find_one(RefreshToken.token == request.refresh_token)
    if db_token:
        db_token.revoked = True
        await db_token.save()
    await log_audit("logout", user_id=str(current_user.id), entity="user", entity_id=str(current_user.id))
    return {"message": "Successfully logged out"}

@router.post("/forgot-password")
async def forgot_password(request: ForgotPassword) -> Any:
    user = await User.find_one(User.email == request.email, User.is_deleted == False)
    if user:
        reset_token = secrets.token_urlsafe(32)
        db_token = PasswordResetToken(
            user_id=str(user.id),
            token=reset_token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=2)
        )
        await db_token.insert()
        await log_audit("password_reset_requested", user_id=str(user.id), entity="user")
    return {"message": "If an account exists, you will receive reset instructions."}

@router.post("/reset-password")
async def reset_password(request: ResetPassword) -> Any:
    db_token = await PasswordResetToken.find_one(
        PasswordResetToken.token == request.token,
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > datetime.now(timezone.utc)
    )
    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user = await User.find_one(User.id == db_token.user_id, User.is_deleted == False)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = security.get_password_hash(request.new_password)
    db_token.used = True
    await user.save()
    await db_token.save()
    await RefreshToken.find(RefreshToken.user_id == str(user.id)).update({"$set": {"revoked": True}})
    await log_audit("password_reset", user_id=str(user.id), entity="user")
    return {"message": "Password reset successful"}

@router.post("/change-password")
async def change_password(current_user: CurrentUser, request: ChangePassword) -> Any:
    if not security.verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    current_user.password_hash = security.get_password_hash(request.new_password)
    await current_user.save()
    await RefreshToken.find(RefreshToken.user_id == str(current_user.id)).update({"$set": {"revoked": True}})
    await log_audit("password_changed", user_id=str(current_user.id), entity="user")
    return {"message": "Password changed successfully"}
