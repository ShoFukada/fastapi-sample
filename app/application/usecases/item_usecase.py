from typing import Optional, List
from app.domain.models.item import Item
from app.domain.repositories.item_repository_interface import ItemRepositoryInterface
from injector import inject

class ItemUseCase:
    @inject
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

    def get_item(self, item_id: int) -> Optional[Item]:
        return self.item_repository.get_item(item_id)

    def get_items(self) -> List[Item]:
        return self.item_repository.get_items()

    def create_item(self, name: str, price: int, discount_rate: float) -> Item:
        new_item = Item(
            id=0,
            name=name,
            price=price,
            discount_rate=discount_rate
        )
        # Repository でDBに保存
        return self.item_repository.create_item(new_item)

    def delete_item(self, item_id: int) -> bool:
        return self.item_repository.delete_item(item_id)