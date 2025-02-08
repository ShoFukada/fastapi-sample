from injector import Injector, Module, provider, singleton, Binder
from app.application.usecases.item_usecase import ItemUseCase
from app.domain.repositories.item_repository_interface import ItemRepositoryInterface
from app.infrastructure.repositories.item_repository import ItemRepository


class AppModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(ItemRepositoryInterface, to=ItemRepository, scope=singleton)
        binder.bind(ItemUseCase, scope=singleton)

injector = Injector([AppModule()])