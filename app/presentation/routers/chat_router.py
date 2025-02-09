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
from app.core.dependencies import get_chat_session_usecase


router = APIRouter(prefix="/chat", tags=["Chat"])

# 今までのセッションの一覧
@router.get("/sessions", response_model=List[ChatSessionResponse])
def list_sessions(usecase: ChatSessionUseCase = Depends(get_chat_session_usecase)):
    sessions = usecase.list_chat_session()
    return [
        ChatSessionResponse(
            session_id=session.id,
            user_id=session.user_id,
            title=session.title,
            created_at=session.created_at
        )
        for session in sessions
    ]
    

# セッション作成
@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(req: CreateSessionRequest, usecase: ChatSessionUseCase = Depends(get_chat_session_usecase)):
    new_session = usecase.create_chat_session(
        user_id=req.user_id,
        title=req.title
    )
    return ChatSessionResponse(
        session_id=new_session.id,
        user_id=new_session.user_id,
        title=new_session.title,
        created_at=new_session.created_at
    )

# やり取り取得
@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def list_messages(session_id: str):
    pass

# チャットapi
# ユーザ質問保存、参照文書検索、回答ストリーミング、回答保存
@router.post("/sessions/{session_id}/messages")
def create_message(session_id: str):
    pass