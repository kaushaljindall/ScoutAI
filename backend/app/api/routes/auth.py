from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import SessionDep, CurrentUser
from app.core import security
from app.core.config import settings
from app.models.user import User, AuditLog
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: SessionDep) -> Any:
    """
    Register a new user.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Audit log
    audit = AuditLog(user_id=user.id, action="user_registered", entity="user", entity_id=user.id)
    db.add(audit)
    db.commit()
    
    return user

@router.post("/login", response_model=Token)
def login_access_token(
    db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token = security.create_access_token(user.id)
    refresh_token = security.create_refresh_token(user.id)
    
    audit = AuditLog(user_id=user.id, action="user_login", entity="user", entity_id=user.id)
    db.add(audit)
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(
    db: SessionDep, refresh_token: str
) -> Any:
    """
    Refresh access token
    """
    try:
        payload = security.jwt.decode(
            refresh_token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except (security.jwt.JWTError, Exception):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    access_token = security.create_access_token(user.id)
    new_refresh_token = security.create_refresh_token(user.id)
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user

@router.post("/logout")
def logout(current_user: CurrentUser, db: SessionDep) -> Any:
    """
    Logout (record in audit log, client handles token clearing)
    """
    audit = AuditLog(user_id=current_user.id, action="user_logout", entity="user", entity_id=current_user.id)
    db.add(audit)
    db.commit()
    return {"message": "Successfully logged out"}
