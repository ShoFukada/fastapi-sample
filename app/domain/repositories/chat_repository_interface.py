# chat_domain→dbのinterface
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.chat import ChatSession, ChatMessage

class ChatSessionRepositoryInterface(ABC):
    @abstractmethod
    def list_chat_session(self) -> List[ChatSession]:
        raise NotImplementedError
    
    @abstractmethod
    def list_chat_session_by_user_id(self, user_id: str) -> List[ChatSession]:
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


class ChatMessageRepositoryInterface(ABC):
    @abstractmethod
    def list_chat_message_by_session_id(self, session_id: str) -> List[ChatMessage]:
        raise NotImplementedError
    
    @abstractmethod
    def create_chat_message(self, chat_message: ChatMessage) -> ChatMessage:
        raise NotImplementedError