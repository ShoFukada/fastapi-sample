from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

# チャットメッセージの役割 (値オブジェクトに近いイメージ)
class ChatRole(str, Enum):
    USER = "user"
    SYSTEM  = "system"
    ASSISTANT = "assistant"

@dataclass
class ChatSession:
    id: str
    user_id: str
    title: str
    created_at: Optional[datetime] = None


# この辺もっとうまくできない？
# 単にfilter json以外のロジックが入る可能性があるためここではクラス、db前ではfilter strにする
@dataclass
class FilterParams:
    created_at_start: Optional[datetime]
    created_at_end: Optional[datetime]

@dataclass
class RetrievedDoc:
    id: str
    chat_message_id: str
    doc_id: str
    content: str
    score: float
    doc_metadata: Dict[str, Any]
    created_at: Optional[datetime] = None


@dataclass
class ChatMessage:
    id: str
    session_id: str
    role: ChatRole
    content: str
    prompt: Optional[Any] = None
    prompt_str: Optional[str] = None
    filter_query: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    retrieved_docs: Optional[List[RetrievedDoc]] = None