
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class User:
    """
    ドメインモデルとしてのユーザ。
    (DBのORMと分離しておく)
    """
    id: str
    email: str
    display_name: Optional[str]
    hashed_password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None