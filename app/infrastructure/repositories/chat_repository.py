from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.models.chat import ChatSession
from app.domain.repositories.chat_repository_interface import ChatSessionRepositoryInterface
from app.infrastructure.db.models import ChatSessionORM

class ChatSessionRepository(ChatSessionRepositoryInterface):
    def __init__(self):
        self._db: Optional[Session] = None

    def set_db_session(self, db: Session) -> None:
        self._db = db

    def list_chat_session(self) -> List[ChatSessionORM]:
        records = self._db.query(ChatSessionORM).all()
        return [
            r.to_entity()
            for r in records
        ]

    def create_chat_session(self, chat_session: ChatSessionORM) -> ChatSessionORM:
        record = ChatSessionORM(
            user_id=chat_session.user_id,
            created_at=chat_session.created_at
        )
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record.to_entity()

    def get_session(self, session_id: str) -> Optional[ChatSessionORM]:
        record = self._db.query(ChatSessionORM).filter(ChatSessionORM.session_id == session_id).first()
        if not record:
            return None
        return record.to_entity()