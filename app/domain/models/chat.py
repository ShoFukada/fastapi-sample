from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

# チャットメッセージの役割 (値オブジェクトに近いイメージ)
class ChatRole(str, Enum):
    USER = "user"
    AI = "ai"

@dataclass
class ChatSession:
    id: str
    user_id: str
    title: str
    created_at: datetime