from typing import Optional, List
from app.domain.models.chat import ChatSession
from app.domain.repositories.chat_repository_interface import ChatSessionRepositoryInterface
from injector import inject

class ChatSessionUseCase:
    @inject
    def __init__(self, chat_session_repository: ChatSessionRepositoryInterface):
        self.chat_session_repository = chat_session_repository

    def list_chat_session(self) -> List[ChatSession]:
        return self.chat_session_repository.list_chat_session()

    def create_chat_session(self, session_id: str, user_id: str) -> ChatSession:
        new_chat_session = ChatSession(
            session_id=session_id,
            user_id=user_id
        )
        return self.chat_session_repository.create_chat_session(new_chat_session)

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        return self.chat_session_repository.get_session(session_id)