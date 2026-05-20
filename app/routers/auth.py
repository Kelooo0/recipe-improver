from fastapi import APIRouter, Depends, status
from app.schemas import User, UserCreate, Token
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import auth_service
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.models import UserModel

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserModel:
    auth_service.check_user_exists(user_data, db)
    return auth_service.register_user(user_data, db)


@router.post("/login", response_model=Token)
def login(
    user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Any:
    user = auth_service.validate_user(user_data.username, user_data.password, db)

    access_token = auth_service.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "Bearer"}
