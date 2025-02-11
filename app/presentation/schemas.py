from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

# Item

class ItemResponse(BaseModel):
    id: str
    name: str
    price: float
    discount_rate: float
    discounted_price: float


class CreateItemRequest(BaseModel):
    name: str
    price: int
    discount_rate: float


# Chat/Session
class CreateSessionRequest(BaseModel):
    # user_id: str
    title: str

class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime

class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"




# Chat/Session/Message
class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: ChatRole
    content: str
    created_at: datetime
    # prompt: Optional[str]
    # filter_query: Optional[FilterQuery]

class RequestFilterParams(BaseModel):
    created_at_start: Optional[datetime] = None
    created_at_end: Optional[datetime] = None
    prefecture: Optional[str] = None
    location: Optional[str] = None

class MessageRequest(BaseModel):
    question: str
    filter_params: Optional[RequestFilterParams] = None

class CreateMessageANdAnswerResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse




# User
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class DecodedTokenData(BaseModel):
    user_id: Optional[str] = None

class UserCreateRequest(BaseModel):
    email: str
    display_name: Optional[str] = None
    password: str

class UserCreateResponse(BaseModel):
    id: str
    email: str
    display_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserReadResponse(BaseModel):
    id: str
    email: str
    display_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserLoginRequest(BaseModel):
    email: str
    password: str