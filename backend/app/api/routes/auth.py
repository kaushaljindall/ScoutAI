import uuid
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import SessionDep, CurrentUser
from app.core import security
from app.core.config import settings
from app.models.user import User, AuditLog, RefreshToken, PasswordResetToken
from app.schemas.user import UserCreate, UserResponse, Token, RefreshTokenRequest, ForgotPassword, ResetPassword, ChangePassword

router = APIRouter()

def log_audit(db: Session, action: str, user_id: uuid.UUID = None, entity: str = None, entity_id: uuid.UUID = None):
    audit = AuditLog(user_id=user_id, action=action, entity=entity, entity_id=entity_id)
    db.add(audit)
    db.commit()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: SessionDep) -> Any:
    """
    Register a new user.
    """
    user = db.query(User).filter(User.email == user_in.email, User.is_deleted == False).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = User(
        email=user_in.email,
        password_hash=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    log_audit(db, action="register", user_id=user.id, entity="user", entity_id=user.id)
    return user

@router.post("/login", response_model=Token)
def login_access_token(
    db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(User.email == form_data.username, User.is_deleted == False).first()
    if not user:
        log_audit(db, action="failed_login", entity="email", details={"email": form_data.username})
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if not security.verify_password(form_data.password, user.password_hash):
        log_audit(db, action="failed_login", user_id=user.id, entity="user", entity_id=user.id)
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    user.last_login = datetime.now(timezone.utc)
    
    access_token = security.create_access_token(user.id)
    refresh_token_str = security.create_refresh_token(user.id)
    
    # Store refresh token in DB
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(db_refresh_token)
    db.commit()
    
    log_audit(db, action="login", user_id=user.id, entity="user", entity_id=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(
    db: SessionDep, request: RefreshTokenRequest
) -> Any:
    """
    Refresh access token
    """
    try:
        payload = security.jwt.decode(
            request.refresh_token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except (security.jwt.JWTError, Exception):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Check if token exists and is not revoked
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == request.refresh_token,
        RefreshToken.revoked == False
    ).first()
    
    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired or invalid")
        
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found or inactive")
        
    # Revoke old refresh token (Token rotation)
    db_token.revoked = True
    
    access_token = security.create_access_token(user.id)
    new_refresh_token_str = security.create_refresh_token(user.id)
    
    new_db_token = RefreshToken(
        user_id=user.id,
        token=new_refresh_token_str,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(new_db_token)
    db.commit()
    
    log_audit(db, action="token_refresh", user_id=user.id, entity="user", entity_id=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token_str,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user

@router.post("/logout")
def logout(current_user: CurrentUser, request: RefreshTokenRequest, db: SessionDep) -> Any:
    """
    Logout and revoke token
    """
    db_token = db.query(RefreshToken).filter(RefreshToken.token == request.refresh_token).first()
    if db_token:
        db_token.revoked = True
        db.commit()
        
    log_audit(db, action="logout", user_id=current_user.id, entity="user", entity_id=current_user.id)
    return {"message": "Successfully logged out"}

@router.post("/forgot-password")
def forgot_password(request: ForgotPassword, db: SessionDep) -> Any:
    """
    Request password reset
    """
    user = db.query(User).filter(User.email == request.email, User.is_deleted == False).first()
    if user:
        reset_token = secrets.token_urlsafe(32)
        db_token = PasswordResetToken(
            user_id=user.id,
            token=reset_token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=2)
        )
        db.add(db_token)
        db.commit()
        # In a real app, send an email with the token here
        log_audit(db, action="password_reset_requested", user_id=user.id, entity="user", entity_id=user.id)
        
    return {"message": "If an account exists, you will receive reset instructions."}

@router.post("/reset-password")
def reset_password(request: ResetPassword, db: SessionDep) -> Any:
    """
    Reset password
    """
    db_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token,
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
    user = db.query(User).filter(User.id == db_token.user_id, User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.password_hash = security.get_password_hash(request.new_password)
    db_token.used = True
    
    # Revoke all refresh tokens
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update({"revoked": True})
    
    db.commit()
    
    log_audit(db, action="password_reset", user_id=user.id, entity="user", entity_id=user.id)
    return {"message": "Password reset successful"}

@router.post("/change-password")
def change_password(current_user: CurrentUser, request: ChangePassword, db: SessionDep) -> Any:
    """
    Change password for authenticated user
    """
    if not security.verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")
        
    current_user.password_hash = security.get_password_hash(request.new_password)
    
    # Revoke all refresh tokens
    db.query(RefreshToken).filter(RefreshToken.user_id == current_user.id).update({"revoked": True})
    
    db.commit()
    log_audit(db, action="password_changed", user_id=current_user.id, entity="user", entity_id=current_user.id)
    
    return {"message": "Password changed successfully"}
