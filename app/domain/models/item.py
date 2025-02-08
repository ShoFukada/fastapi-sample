# 外部に依存しないmodel定義, dataclassを使う
# dataclassは、__init__や__repr__などの特殊メソッドを自動生成する

from dataclasses import dataclass

@dataclass
class Item:
    id: int
    name: str
    price: int
    discount_rate: float

    def get_discounted_price(self) -> int:
        return self.price * (1 - self.discount_rate)