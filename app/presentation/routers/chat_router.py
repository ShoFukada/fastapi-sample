from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.infrastructure.db.session import get_db
from app.presentation.schemas import ChatSessionResponse, CreateSessionRequest, MessageResponse, MessageRequest, RequestFilterParams, CreateMessageANdAnswerResponse
from app.application.usecases.chat_usecase import ChatSessionUseCase, ChatMessageUseCase
from app.infrastructure.repositories.chat_repository import ChatSessionRepository
from sqlalchemy.orm import Session
from app.core.di_container import injector
from app.core.dependencies import get_chat_session_usecase, get_chat_message_usecase, get_current_user_dependency
from app.domain.models.chat import FilterParams

router = APIRouter(prefix="/chat", tags=["Chat"])

# 今までのセッションの一覧 TODO user_idで絞り込み
@router.get("/sessions", response_model=List[ChatSessionResponse])
def list_sessions(usecase: ChatSessionUseCase = Depends(get_chat_session_usecase), current_user = Depends(get_current_user_dependency)):
    sessions = usecase.list_chat_session_by_user_id(user_id=current_user.id)
    return [
        ChatSessionResponse(
            id=session.id,
            user_id=session.user_id,
            title=session.title,
            created_at=session.created_at
        )
        for session in sessions
    ]
    

# セッション作成
@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(req: CreateSessionRequest, usecase: ChatSessionUseCase = Depends(get_chat_session_usecase), current_user = Depends(get_current_user_dependency)):
    new_session = usecase.create_chat_session(
        user_id=current_user.id,
        title=req.title
    )
    return ChatSessionResponse(
        id=new_session.id,
        user_id=new_session.user_id,
        title=new_session.title,
        created_at=new_session.created_at
    )

# セッション削除
@router.delete("/sessions/{session_id}", response_model=bool)
def delete_session(session_id: str, usecase: ChatSessionUseCase = Depends(get_chat_session_usecase)):
    result = usecase.delete_session(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    return result

# やり取り取得
@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def list_messages(session_id: str, usecase: ChatMessageUseCase = Depends(get_chat_message_usecase)):
    messages = usecase.list_chat_message(session_id)
    return [
        MessageResponse(
            id=message.id,
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at
        )
        for message in messages
    ]

# チャットapi
# ユーザ質問保存、参照文書検索、回答、、回答保存
@router.post("/sessions/{session_id}/messages")
def create_message_and_answer(req: MessageRequest, session_id: str, usecase: ChatMessageUseCase = Depends(get_chat_message_usecase), current_user = Depends(get_current_user_dependency)):

    filter_params = None
    if req.filter_params:
        filter_params = FilterParams(
            created_at_start=req.filter_params.created_at_start,
            created_at_end=req.filter_params.created_at_end,
            prefecture=req.filter_params.prefecture,
            location=req.filter_params.location
        )

    user_message, assistant_message = usecase.generate_answer(
        session_id=session_id,
        message=req.question,
        filter_params=filter_params
    )
    return CreateMessageANdAnswerResponse(
        user_message=MessageResponse(
            id=user_message.id,
            session_id=user_message.session_id,
            role=user_message.role,
            content=user_message.content,
            created_at=user_message.created_at
        ),
        assistant_message=MessageResponse(
            id=assistant_message.id,
            session_id=assistant_message.session_id,
            role=assistant_message.role,
            content=assistant_message.content,
            created_at=assistant_message.created_at
        )
    )

@router.post("/sessions/{session_id}/messages/stream")
def create_message_and_answer_stream(
    session_id: str,
    req: MessageRequest,
    usecase: ChatMessageUseCase = Depends(get_chat_message_usecase),
    current_user = Depends(get_current_user_dependency)
):
    """
    ストリーミングで回答を返すエンドポイント
    """

    # 1. FilterParams に変換
    filter_params = None
    if req.filter_params:
        filter_params = FilterParams(
            created_at_start=req.filter_params.created_at_start,
            created_at_end=req.filter_params.created_at_end,
            prefecture=req.filter_params.prefecture,
            location=req.filter_params.location
        )

    # 2. ジェネレーターを作る (SSEの形式に整形)
    def event_stream():
        # usecase.generate_answer_stream() が (event_type, payload) のタプルを yield する想定
        stream_gen = usecase.generate_answer_stream(session_id, req.question, filter_params)
        for event_type, payload in stream_gen:
            if event_type == "user_message_id_event":
                yield f"event: user_message_id\ndata: {payload}\n\n"
            elif event_type == "assistant_chunk":
                yield f"event: chunk\ndata: {payload}\n\n"
            elif event_type == "assistant_message_id_event":
                yield f"event: assistant_message_id\ndata: {payload}\n\n"

        # ストリーミング終了
        yield "event: done\ndata: end\n\n"

    # 3. StreamingResponse で SSE を返す
    return StreamingResponse(event_stream(), media_type="text/event-stream")