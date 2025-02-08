from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.item import Item

class ItemRepositoryInterface(ABC):
    @abstractmethod
    def get_item(self, item_id: int) -> Optional[Item]:
        raise NotImplementedError
    
    @abstractmethod
    def get_items(self) ->  List[Item]:
        raise NotImplementedError
    
    @abstractmethod
    def create_item(self, item: Item) -> Item:
        raise NotImplementedError
    
    @abstractmethod
    def delete_item(self, item_id: int) -> bool:
        raise NotImplementedError