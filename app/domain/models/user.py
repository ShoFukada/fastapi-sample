
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class User:
    """
    ドメインモデルとしてのユーザ。
    (DBのORMと分離しておく)
    """
    email: str
    display_name: Optional[str]
    hashed_password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: str = field(default_factory=lambda: str(uuid4()))