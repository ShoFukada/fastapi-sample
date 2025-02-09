from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.infrastructure.db.session import get_db
from app.presentation.schemas import ChatSessionResponse, CreateSessionRequest, MessageResponse
from app.application.usecases.chat_usecase import ChatSessionUseCase
from app.infrastructure.repositories.chat_repository import ChatSessionRepository
from sqlalchemy.orm import Session
from app.core.di_container import injector

router = APIRouter(prefix="/chat", tags=["Chat"])

def get_chat_session_usecase(db: Session = Depends(get_db)) -> ChatSessionUseCase:
    usecase = injector.get(ChatSessionUseCase)
    if isinstance(usecase.chat_session_repository, ChatSessionRepository):
        usecase.chat_session_repository.set_db_session(db)
    return usecase

# 今までのセッションの一覧
@router.get("/sessions", response_model=List[ChatSessionResponse])
def list_sessions(usecase: ChatSessionUseCase = Depends(get_chat_session_usecase)):
    sessions = usecase.list_chat_session()
    return sessions
    

# セッション作成
@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(req: CreateSessionRequest, usecase: ChatSessionUseCase = Depends(get_chat_session_usecase)):
    new_session = usecase.create_chat_session(
        session_id=req.session_id,
        user_id=req.user_id
    )
    return new_session

# やり取り取得
@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def list_messages(session_id: str):
    pass

# チャットapi
# ユーザ質問保存、参照文書検索、回答ストリーミング、回答保存
@router.post("/sessions/{session_id}/messages")
def create_message(session_id: str):
    pass