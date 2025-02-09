# app/presentation/routers/item_router.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db
from app.presentation.schemas import ItemResponse, CreateItemRequest
from app.domain.models.item import Item

# DIコンテナ
from app.core.di_container import injector
from app.application.usecases.item_usecase import ItemUseCase
from app.infrastructure.repositories.item_repository import ItemRepository

router = APIRouter(prefix="/items", tags=["Items"])

def get_item_usecase(db: Session = Depends(get_db)) -> ItemUseCase:
    """
    UseCase を Injector から取り出し、その中の Repository に
    リクエストごとの db session を注入するための関数
    """
    # singletonについては初回injector.get()でインスタンスが生成され、以降はそれを返す
    usecase = injector.get(ItemUseCase)
    # Repository が ItemRepository ならセッションをセット
    if isinstance(usecase.item_repository, ItemRepository):
        usecase.item_repository.set_db_session(db)
    return usecase

@router.get("/", response_model=List[ItemResponse])
def list_items(usecase: ItemUseCase = Depends(get_item_usecase)):
    items = usecase.get_items()
    return [
        ItemResponse(
            id=item.id,
            name=item.name,
            price=item.price,
            discount_rate=item.discount_rate,
            discounted_price=item.get_discounted_price()
        )
        for item in items
    ]

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, usecase: ItemUseCase = Depends(get_item_usecase)):
    item = usecase.get_item(item_id)
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
def create_item(req: CreateItemRequest, usecase: ItemUseCase = Depends(get_item_usecase)):
    new_item = usecase.create_item(
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
def delete_item(item_id: int, usecase: ItemUseCase = Depends(get_item_usecase)):
    success = usecase.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted"}