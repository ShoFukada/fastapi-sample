from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    discount_rate: float
    discounted_price: float


class CreateItemRequest(BaseModel):
    name: str
    price: int
    discount_rate: float