from fastapi import HTTPException, status
from app.schemas import User, UserCreate
from app.models import UserModel
from sqlalchemy.orm import Session
import bcrypt
from datetime import datetime, timezone, timedelta
import jwt
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


class AuthService:
    @staticmethod
    def check_user_exists(user_data: UserCreate, db: Session) -> None:
        existing_user = (
            db.query(UserModel).filter(UserModel.email == user_data.email).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

    @staticmethod
    def get_pw_hash(password: str) -> str:
        pw_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        pw_hashed = bcrypt.hashpw(pw_bytes, salt)
        return pw_hashed.decode("utf-8")

    def register_user(self, user_data: UserCreate, db: Session) -> UserModel:
        pw_hashed = self.get_pw_hash(user_data.password)

        new_user = UserModel(email=user_data.email, password=pw_hashed)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def verify_password(password, password_hash) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def validate_user(self, email: str, password: str, db: Session) -> UserModel:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authentication": "Bearer"},
            )
        return user

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


auth_service = AuthService()
