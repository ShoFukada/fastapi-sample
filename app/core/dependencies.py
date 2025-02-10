from app.core.di_container import injector
from app.infrastructure.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.auth import oauth2_scheme, decode_access_token
from app.domain.models.user import User
from app.presentation.schemas import DecodedTokenData
from fastapi import HTTPException

from app.application.usecases.item_usecase import ItemUseCase
from app.infrastructure.repositories.item_repository import ItemRepository
from app.application.usecases.chat_usecase import ChatSessionUseCase
from app.infrastructure.repositories.chat_repository import ChatSessionRepository
from app.application.usecases.user_usecase import UserUseCase
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.usecases.chat_usecase import ChatMessageUseCase
from app.infrastructure.repositories.chat_repository import ChatMessageRepository

def get_item_usecase(db: Session = Depends(get_db)):
    usecase = injector.get(ItemUseCase)
    if isinstance(usecase.item_repository, ItemRepository):
        usecase.item_repository.set_db_session(db)
    return usecase

def get_chat_session_usecase(db: Session = Depends(get_db)):
    usecase = injector.get(ChatSessionUseCase)
    if isinstance(usecase.chat_session_repository, ChatSessionRepository):
        usecase.chat_session_repository.set_db_session(db)
    return usecase

def get_chat_message_usecase(db: Session = Depends(get_db)):
    usecase = injector.get(ChatMessageUseCase)
    if isinstance(usecase.chat_message_repository, ChatMessageRepository):
        usecase.chat_message_repository.set_db_session(db)
    return usecase

def get_user_usecase(db: Session = Depends(get_db)):
    usecase = injector.get(UserUseCase)
    if isinstance(usecase.user_repository, UserRepository):
        usecase.user_repository.set_db_session(db)
    return usecase

def get_current_user_dependency(token: str = Depends(oauth2_scheme), user_usecase: UserUseCase = Depends(get_user_usecase)) -> User:
    try:
        token_data: DecodedTokenData = decode_access_token(token)
        user = user_usecase.get_user_by_id(token_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")