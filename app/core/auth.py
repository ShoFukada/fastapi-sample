# app/core/auth.py

from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

from app.presentation.schemas import DecodedTokenData  # TokenDataに user_id を持たせる

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
print("SECRET_KEY, ALGORITHM")
print(SECRET_KEY, ALGORITHM)
# 環境変数が文字列の場合は int に変換
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 用の依存関数 (tokenUrl="token" は例)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/signin")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """平文とハッシュを突合"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """平文パスワードをハッシュ"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT を発行。payloadに user_id を含める想定"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> DecodedTokenData:
    """アクセストークンをデコードし、TokenData を返す (sub=user_id)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token: sub is None")
        return DecodedTokenData(user_id=user_id)
    except JWTError as e:
        print(e)
        raise ValueError("Invalid token")