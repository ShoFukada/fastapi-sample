# app/infrastructure/repositories/item_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.models.item import Item
from app.domain.repositories.item_repository_interface import ItemRepositoryInterface
from app.infrastructure.db.models import ItemORM

class ItemRepository(ItemRepositoryInterface):
    """
    ここでは、コンストラクタで DB を受け取る設計だが、
    DIコンテナではまだ session を注入していない。
    代わりに set_db_session() であと注入する方針。
    """
    def __init__(self):
        self._db: Optional[Session] = None

    def set_db_session(self, db: Session) -> None:
        self._db = db

    def get_item(self, item_id: int) -> Optional[Item]:
        record = self._db.query(ItemORM).filter(ItemORM.id == item_id).first()
        if not record:
            return None
        return record.to_entity()

    def get_items(self) -> List[Item]:
        records = self._db.query(ItemORM).all()
        return [
            r.to_entity()
            for r in records
        ]

    def create_item(self, item: Item) -> Item:
        record = ItemORM(
            name=item.name,
            price=item.price,
            discount_rate=item.discount_rate
        )
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record.to_entity()

    def delete_item(self, item_id: int) -> bool:
        record = self._db.query(ItemORM).filter(ItemORM.id == item_id).first()
        if not record:
            return False
        self._db.delete(record)
        self._db.commit()
        return True