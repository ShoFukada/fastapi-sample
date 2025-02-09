from injector import Injector, Module, provider, singleton, Binder
from app.application.usecases.item_usecase import ItemUseCase
from app.domain.repositories.item_repository_interface import ItemRepositoryInterface
from app.infrastructure.repositories.item_repository import ItemRepository

from app.application.usecases.chat_usecase import ChatSessionUseCase
from app.domain.repositories.chat_repository_interface import ChatSessionRepositoryInterface
from app.infrastructure.repositories.chat_repository import ChatSessionRepository

from app.application.usecases.user_usecase import UserUseCase
from app.domain.repositories.user_repository_interface import UserRepositoryInterface
from app.infrastructure.repositories.user_repository import UserRepository


class AppModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(ItemRepositoryInterface, to=ItemRepository, scope=singleton)
        binder.bind(ItemUseCase, scope=singleton)

        binder.bind(ChatSessionRepositoryInterface, to=ChatSessionRepository, scope=singleton)
        binder.bind(ChatSessionUseCase, scope=singleton)

        binder.bind(UserRepositoryInterface, to=UserRepository, scope=singleton)
        binder.bind(UserUseCase, scope=singleton)

injector = Injector([AppModule()])