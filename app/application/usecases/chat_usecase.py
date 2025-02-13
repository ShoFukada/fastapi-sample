from typing import Optional, List, Tuple, Generator
from app.domain.models.chat import ChatSession, ChatMessage, FilterParams, ChatRole
from app.domain.repositories.chat_repository_interface import ChatSessionRepositoryInterface, ChatMessageRepositoryInterface
from app.domain.services.chat_service_interface import ChatMessageServiceInterface
from injector import inject

class ChatSessionUseCase:
    @inject
    def __init__(self, chat_session_repository: ChatSessionRepositoryInterface):
        self.chat_session_repository = chat_session_repository

    def list_chat_session(self) -> List[ChatSession]:
        return self.chat_session_repository.list_chat_session()
    
    def list_chat_session_by_user_id(self, user_id: str) -> List[ChatSession]:
        return self.chat_session_repository.list_chat_session_by_user_id(user_id)

    def create_chat_session(self, user_id: str, title: Optional[str]) -> ChatSession:
        new_chat_session = ChatSession(
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
            session_id=session_id,
            user_id=user_id,
            message=message
        )
        return self.chat_message_repository.create_chat_message(new_chat_message)
    
    def generate_answer(self, session_id: str, message: str, filter_params: Optional[FilterParams]) -> Tuple[ChatMessage, ChatMessage]:
        # docsを取得
        # プロンプト作成
        # メッセージ生成
        user_message = self.chat_message_service.build_user_message(session_id, message, self.list_chat_message(session_id), filter_params)
        # db保存
        saved_user_message = self.chat_message_repository.create_chat_message(user_message)
        # 回答生成
        assistant_message_content = self.chat_message_service.generate_answer(user_message)
        assistant_message = ChatMessage(
            session_id=session_id,
            role=ChatRole.ASSISTANT,
            content=assistant_message_content
        )
        # db保存
        saved_assistant_message = self.chat_message_repository.create_chat_message(assistant_message)
        return (saved_user_message, saved_assistant_message)
    
    def generate_answer_stream(self, session_id: str, message: str, filter_params: Optional[FilterParams]) -> Generator[Tuple[str, str], None, None]:
        user_message = self.chat_message_service.build_user_message(session_id, message, self.list_chat_message(session_id), filter_params)
        # db保存
        saved_user_message = self.chat_message_repository.create_chat_message(user_message)
        user_message_id = saved_user_message.id
        yield ("user_message_id_event", user_message_id)

        partial_content = ""
        for chunk in self.chat_message_service.generate_answer_stream(user_message):
            yield ("assistant_chunk", chunk)
            partial_content += chunk
        
        assistant_message_content = partial_content
        assistant_message = ChatMessage(
            session_id=session_id,
            role=ChatRole.ASSISTANT,
            content=assistant_message_content
        )
        # db保存
        saved_assistant_message = self.chat_message_repository.create_chat_message(assistant_message)
        yield ("assistant_message_id_event", saved_assistant_message.id)