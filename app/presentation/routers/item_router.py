from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.usecases.item_usecase import ItemUseCase
from app.infrastructure.repositories.item_repository import ItemRepository
from app.infrastructure.db.session import get_db
from app.presentation.schemas import ItemResponse, CreateItemRequest
from fastapi import HTTPException
from typing import List
from app.domain.models.item import Item

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=List[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    usecase = ItemUseCase(ItemRepository(db))
    items: List[Item] = usecase.get_items()
    # ドメインモデル → レスポンスに変換
    return [
        ItemResponse(
            id=item.id,
            name=item.name,
            price=item.price,
            discount_rate=item.discount_rate,
            discounted_price=item.get_discounted_price()
        ) for item in items
    ]

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    usecase = ItemUseCase(ItemRepository(db))
    item: Item = usecase.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemResponse(
        id=item.id,
        name=item.name,
        price=item.price,
        discount_rate=item.discount_rate,
        discounted_price=item.get_discounted_price()
    )

@router.post("/", response_model=ItemResponse)
def create_item(req: CreateItemRequest, db: Session = Depends(get_db)):
    usecase = ItemUseCase(ItemRepository(db))
    new_item: Item = usecase.create_item(
        name=req.name,
        price=req.price,
        discount_rate=req.discount_rate
    )
    return ItemResponse(
        id=new_item.id,
        name=new_item.name,
        price=new_item.price,
        discount_rate=new_item.discount_rate,
        discounted_price=new_item.get_discounted_price()
    )

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    usecase = ItemUseCase(ItemRepository(db))
    success = usecase.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted"}