# chat_service_interface
from abc import ABC, abstractmethod
from typing import Optional, List, Generator
from app.domain.models.chat import ChatSession, ChatMessage

# ここpresentation層でok?
from app.presentation.schemas import RequestFilterParams

class ChatMessageServiceInterface(ABC):
    """
    rag関連のinterface
    """
    @abstractmethod
    def generate_answer(self, user_message: ChatMessage) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def generate_answer_stream(self, user_content: str, filter_params: Optional[RequestFilterParams]) -> Generator[str, None, None]:
        raise NotImplementedError
    
    @abstractmethod
    def build_user_message(self, session_id: str, user_content: str, past_messages: List[ChatMessage], filter_params: Optional[RequestFilterParams]) -> ChatMessage:
        raise NotImplementedError

    # メッセージを生成するメソッド