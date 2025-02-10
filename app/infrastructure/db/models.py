from sqlalchemy import Column, String, DateTime, Float, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.db.session import Base
import uuid
from sqlalchemy.sql import func

# User
class UserORM(Base):
    """
    本来はユーザのDBモデルが既にある想定ですが、
    ここでは簡易的にサンプルをおいておく
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_entity(self):
        from app.domain.models.user import User
        return User(
            id=self.id,
            email=self.email,
            display_name=self.display_name,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


# Item
class ItemORM(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    discount_rate = Column(Float, nullable=True)

    def to_entity(self):
        from app.domain.models.item import Item
        return Item(
            id=self.id,
            name=self.name,
            price=self.price,
            discount_rate=self.discount_rate
        )
    

# ChatSession
class ChatSessionORM(Base):
    __tablename__ = "chat_session"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # user リレーション (ユーザテーブルを参照)
    # (※ユーザのORMクラスが "User" として定義されている想定)
    user = relationship("UserORM", backref="chat_sessions")

    # セッションに紐づくメッセージのリレーション
    messages = relationship("ChatMessageORM", back_populates="session")

    def to_entity(self):
        from app.domain.models.chat import ChatSession
        return ChatSession(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            created_at=self.created_at
        )


class ChatMessageORM(Base):
    __tablename__ = "chat_message"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_session.id"), nullable=False)
    role = Column(Enum("user", "assistant", "system", name="chat_role"), nullable=False)
    content = Column(Text, nullable=False)
    prompt = Column(Text, nullable=True)
    filter_query = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # リレーション
    session = relationship("ChatSessionORM", back_populates="messages")
    retrieved_docs = relationship("RetrievedDocORM", back_populates="chat_message")

    def to_entity(self):
        from app.domain.models.chat import ChatMessage, ChatRole

        domain_msg = ChatMessage(
            id=self.id,
            session_id=self.session_id,
            role=ChatRole(self.role),
            content=self.content,
            prompt_str=self.prompt,
            filter_query=self.filter_query,
            created_at=self.created_at,
            retrieved_docs=[]
        )

        if self.retrieved_docs:
            domain_msg.retrieved_docs = [doc_orm.to_entity() for doc_orm in self.retrieved_docs]

        return domain_msg


class RetrievedDocORM(Base):
    __tablename__ = "retrieved_docs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_message_id = Column(String, ForeignKey("chat_message.id"), nullable=False)
    doc_id = Column(String, nullable=False)  # vector store 上のドキュメントID
    content = Column(Text, nullable=True)  # 実際のドキュメント本文
    score = Column(Float, nullable=True)  # 類似度など
    doc_metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # ChatMessage と双方向のリレーション
    chat_message = relationship("ChatMessageORM", back_populates="retrieved_docs")

    def to_entity(self):
        from app.domain.models.chat import RetrievedDoc
        return RetrievedDoc(
            id=self.id,
            chat_message_id=self.chat_message_id,
            doc_id=self.doc_id,
            content=self.content,
            score=self.score,
            doc_metadata=self.doc_metadata,
            created_at=self.created_at
        )