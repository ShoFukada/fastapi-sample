# chat_domain→dbのinterface
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.chat import ChatSession

class ChatSessionRepositoryInterface(ABC):
    @abstractmethod
    def list_chat_session(self) -> List[ChatSession]:
        raise NotImplementedError
    
    @abstractmethod
    def create_chat_session(self, chat_session: ChatSession) -> ChatSession:
        raise NotImplementedError
    
    @abstractmethod
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        raise NotImplementedError
    
    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        raise NotImplementedError