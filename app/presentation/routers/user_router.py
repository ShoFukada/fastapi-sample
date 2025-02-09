from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from sqlalchemy.orm import Session

# DI dependencies
from app.core.dependencies import get_user_usecase, get_current_user_dependency
from app.application.usecases.user_usecase import UserUseCase

# スキーマ
from app.presentation.schemas import (
    UserCreateRequest,
    UserCreateResponse,
    UserReadResponse,
    UserLoginRequest,
    TokenResponse
)
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.models.user import User
from app.core.auth import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserCreateResponse)
def signup(req: UserCreateRequest, usecase: UserUseCase = Depends(get_user_usecase)):
    new_user = usecase.create_user(
        email=req.email,
        display_name=req.display_name,
        password=req.password
    )
    return UserCreateResponse(
        id=new_user.id,
        email=new_user.email,
        display_name=new_user.display_name,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
    )

@router.post("/signin", response_model=TokenResponse)
def signin(req: OAuth2PasswordRequestForm = Depends(), usecase: UserUseCase = Depends(get_user_usecase)):
    user = usecase.authenticate_user(
        email=req.username,
        password=req.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    access_token = create_access_token(data={"sub": user.id})
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserCreateResponse)
def get_me(current_user: User = Depends(get_current_user_dependency)):
    return UserReadResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )