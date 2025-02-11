from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.chat import ChatSession, ChatMessage
from app.domain.repositories.chat_repository_interface import ChatSessionRepositoryInterface, ChatMessageRepositoryInterface
from app.infrastructure.db.models import ChatSessionORM, ChatMessageORM, RetrievedDocORM

class ChatSessionRepository(ChatSessionRepositoryInterface):
    def __init__(self):
        self._db: Optional[Session] = None

    def set_db_session(self, db: Session) -> None:
        self._db = db

    def list_chat_session(self) -> List[ChatSessionORM]:
        records = self._db.query(ChatSessionORM).filter(ChatSessionORM.is_deleted == False).all()
        return [
            r.to_entity()
            for r in records
        ]
    
    def list_chat_session_by_user_id(self, user_id: str) -> List[ChatSessionORM]:
        records = self._db.query(ChatSessionORM).filter(ChatSessionORM.user_id == user_id, ChatSessionORM.is_deleted == False).all()
        return [
            r.to_entity()
            for r in records
        ]

    def create_chat_session(self, chat_session: ChatSession) -> ChatSessionORM:
        record = ChatSessionORM(
            id=chat_session.id,
            user_id=chat_session.user_id,
            title=chat_session.title,
            created_at=chat_session.created_at
        )
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record.to_entity()

    def get_session(self, session_id: str) -> Optional[ChatSessionORM]:
        record = self._db.query(ChatSessionORM).filter(ChatSessionORM.id == session_id).first()
        if not record:
            return None
        return record.to_entity()
    
    def delete_session(self, session_id: str) -> bool:
        record = (
            self._db.query(ChatSessionORM)
            .filter(ChatSessionORM.id == session_id)
            .first()
        )
        if not record:
            return False

        # ソフトデリート (is_deleted を True に)
        record.is_deleted = True
        self._db.commit()
        return True


class ChatMessageRepository(ChatMessageRepositoryInterface):
    def __init__(self):
        self._db: Optional[Session] = None

    def set_db_session(self, db: Session) -> None:
        self._db = db

    def list_chat_message_by_session_id(self, session_id: str) -> List[ChatMessage]:
        records = self._db.query(ChatMessageORM).filter(ChatMessageORM.session_id == session_id).all()
        return [
            r.to_entity()
            for r in records
        ]

    def create_chat_message(self, chat_message: ChatMessage) -> ChatMessage:
        # 1) ChatMessageORM を生成
        msg_orm = ChatMessageORM(
            id=chat_message.id,
            session_id=chat_message.session_id,
            role=chat_message.role.value,
            content=chat_message.content,
            prompt=chat_message.prompt_str,
            filter_query=chat_message.filter_query,
            created_at=chat_message.created_at
        )
        self._db.add(msg_orm)
        self._db.commit()
        self._db.refresh(msg_orm)

        # 2) retrieved_docs があれば保存
        if chat_message.retrieved_docs:
            for rd in chat_message.retrieved_docs:
                rd_orm = RetrievedDocORM(
                    id=rd.id,
                    chat_message_id=msg_orm.id,
                    doc_id=rd.doc_id,
                    content=rd.content,
                    score=rd.score,
                    doc_metadata=rd.doc_metadata,
                )
                self._db.add(rd_orm)
            self._db.commit()
            self._db.refresh(msg_orm)

        saved_msg = msg_orm.to_entity()
        if msg_orm.retrieved_docs:
            saved_msg.retrieved_docs = [rdo.to_entity() for rdo in msg_orm.retrieved_docs]
        return saved_msg