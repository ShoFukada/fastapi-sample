from typing import Optional, List
from app.domain.models.chat import ChatSession, ChatMessage, FilterParams
from app.domain.repositories.chat_repository_interface import ChatSessionRepositoryInterface, ChatMessageRepositoryInterface
from app.domain.services.chat_service_interface import ChatMessageServiceInterface
from injector import inject

class ChatSessionUseCase:
    @inject
    def __init__(self, chat_session_repository: ChatSessionRepositoryInterface):
        self.chat_session_repository = chat_session_repository

    def list_chat_session(self) -> List[ChatSession]:
        return self.chat_session_repository.list_chat_session()
    
    # TODO list_chat_session_by_user_id
    def list_chat_session_by_user_id(self, user_id: str) -> List[ChatSession]:
        return self.chat_session_repository.list_chat_session_by_user_id(user_id)

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

class ChatMessageUseCase:
    @inject
    def __init__(self, chat_message_repository: ChatMessageRepositoryInterface, chat_message_service: ChatMessageServiceInterface):
        self.chat_message_repository = chat_message_repository
        self.chat_message_service = chat_message_service

    def list_chat_message(self, session_id: str) -> List[ChatMessage]:
        return self.chat_message_repository.list_chat_message_by_session_id(session_id)

    def create_chat_message(self, session_id: str, user_id: str, message: str) -> ChatMessage:
        new_chat_message = ChatMessage(
            message_id=0,
            session_id=session_id,
            user_id=user_id,
            message=message
        )
        return self.chat_message_repository.create_chat_message(new_chat_message)
    
    def generate_answer(self, session_id: str, message: str, filter_params: Optional[FilterParams]) -> str:
        # docsを取得
        # プロンプト作成
        # メッセージ生成
        user_message = self.chat_message_service.build_user_message(message, self.list_chat_message(session_id), filter_params)
        # db保存
        self.chat_message_repository.create_chat_message(user_message)
        # 回答生成
        return self.chat_message_service.generate_answer(user_message)


