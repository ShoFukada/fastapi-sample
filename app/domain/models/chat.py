from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import uuid4

# チャットメッセージの役割 (値オブジェクトに近いイメージ)
class ChatRole(str, Enum):
    USER = "user"
    SYSTEM  = "system"
    ASSISTANT = "assistant"

@dataclass
class ChatSession:
    user_id: str
    title: str
    created_at: Optional[datetime] = None
    id: str = field(default_factory=lambda: str(uuid4()))


# この辺もっとうまくできない？
# 単にfilter json以外のロジックが入る可能性があるためここではクラス、db前ではfilter strにする
@dataclass
class FilterParams:
    created_at_start: Optional[datetime] = None
    created_at_end: Optional[datetime] = None
    prefecture: Optional[str] = None
    location: Optional[str] = None

@dataclass
class RetrievedDoc:
    doc_id: str
    content: str
    score: float
    doc_metadata: Dict[str, Any]
    chat_message_id: Optional[str] = None
    created_at: Optional[datetime] = None
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class ChatMessage:
    session_id: str
    role: ChatRole
    content: str
    prompt: Optional[Any] = None
    prompt_str: Optional[str] = None
    filter_query: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    retrieved_docs: Optional[List[RetrievedDoc]] = None
    id: str = field(default_factory=lambda: str(uuid4()))