from injector import Injector, Module, provider, singleton, Binder
from app.application.usecases.item_usecase import ItemUseCase
from app.domain.repositories.item_repository_interface import ItemRepositoryInterface
from app.infrastructure.repositories.item_repository import ItemRepository

from app.application.usecases.chat_usecase import ChatSessionUseCase, ChatMessageUseCase
from app.domain.repositories.chat_repository_interface import ChatSessionRepositoryInterface, ChatMessageRepositoryInterface
from app.infrastructure.repositories.chat_repository import ChatSessionRepository, ChatMessageRepository

from app.application.usecases.user_usecase import UserUseCase
from app.domain.repositories.user_repository_interface import UserRepositoryInterface
from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.services.chat_service_interface import ChatMessageServiceInterface
from app.infrastructure.services.chat_service import ChatMessageService


class AppModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(ItemRepositoryInterface, to=ItemRepository, scope=singleton)
        binder.bind(ItemUseCase, scope=singleton)

        binder.bind(ChatSessionRepositoryInterface, to=ChatSessionRepository, scope=singleton)
        binder.bind(ChatSessionUseCase, scope=singleton)

        binder.bind(UserRepositoryInterface, to=UserRepository, scope=singleton)
        binder.bind(UserUseCase, scope=singleton)

        binder.bind(ChatMessageServiceInterface, to=ChatMessageService, scope=singleton)
        binder.bind(ChatMessageRepositoryInterface, to=ChatMessageRepository, scope=singleton)
        binder.bind(ChatMessageUseCase, scope=singleton)


injector = Injector([AppModule()])