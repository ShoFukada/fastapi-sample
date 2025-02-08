from sqlalchemy.orm import Session
from typing import Optional, List

from app.domain.repositories.item_repository_interface import ItemRepositoryInterface
from app.domain.models.item import Item
from app.infrastructure.db.models.item import ItemORM

class ItemRepository(ItemRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_item(self, item_id: int) -> Optional[Item]:
        record = self.db.query(ItemORM).filter(ItemORM.id == item_id).first()
        if not record:
            return None
        return Item(
            id=record.id,
            name=record.name,
            price=record.price,
            discount_rate=record.discount_rate
        )
    
    def get_items(self) ->  List[Item]:
        records = self.db.query(ItemORM).all()
        return [Item(
            id=record.id,
            name=record.name,
            price=record.price,
            discount_rate=record.discount_rate
        ) for record in records]
    
    def create_item(self, item: Item) -> Item:
        record = ItemORM(
            name=item.name,
            price=item.price,
            discount_rate=item.discount_rate
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return Item(
            id=record.id,
            name=record.name,
            price=record.price,
            discount_rate=record.discount_rate
        )
    
    def delete_item(self, item_id: int) -> bool:
        record = self.db.query(ItemORM).filter(ItemORM.id == item_id).first()
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True