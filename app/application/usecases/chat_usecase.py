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

    def create_chat_session(self, user_id: str, title: Optional[str]) -> ChatSession:
        new_chat_session = ChatSession(
            session_id=0,
            user_id=user_id,
            title=title
        )
        return self.chat_session_repository.create_chat_session(new_chat_session)

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        return self.chat_session_repository.get_session(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        return self.chat_session_repository.delete_session(session_id)