# langchain関連の処理を行うサービス
from app.domain.services.chat_service_interface import ChatMessageServiceInterface
from app.domain.models.chat import ChatMessage, RetrievedDoc, ChatRole, FilterParams
from typing import Optional, List, Generator, Tuple
from langchain.schema import Document
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from dotenv import load_dotenv
import os

load_dotenv()

# TODO 設定値の安全性をconfig.pyとかで確認する

class ChatMessageService(ChatMessageServiceInterface):
    def __init__(self):
        self.pinecone = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY"),
        )
        index_name = os.getenv("PINECONE_INDEX_NAME")
        index = self.pinecone.Index(index_name)
        emmbedding_model = os.getenv("EMBEDDING_MODEL_NAME")
        embeddings = OpenAIEmbeddings(model=emmbedding_model, api_key=os.getenv("OPENAI_API_KEY"))
        self.vector_store = PineconeVectorStore(index, embeddings)
        self.model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_NAME"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=int(os.getenv("OPENAI_TEMPERATURE")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS")),
        )
        self.system_prompt = os.getenv("OPENAI_SYSTEM_PROMPT")
        self.user_prompt = os.getenv("OPENAI_USER_PROMPT")
        self.prompt = ChatPromptTemplate(
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_messages"),
            ("user", self.user_prompt),
        )

    def generate_answer(self, user_message: ChatMessage) -> str:
        answer = self.model.invoke(user_message.prompt)
        return answer
    
    def generate_answer_stream(self, user_message: ChatMessage) -> Generator[str, None, None]:
        pass
    
    def build_user_message(self, session_id: str, user_content: str, past_messages: List[ChatMessage], filter_params: Optional[FilterParams]) -> ChatMessage:
        """
        ユーザメッセージを作成
        """
        # 1 ドキュメント取得
        filter = self._build_filter(filter_params)
        documents = self._search_pinecone(user_content, filter)

        # 2 プロンプト作成
        context_str = self._build_context(documents)
        question = user_content
        chat_messages = self._build_chat_messages(past_messages)
        prompt_data = {
            "chat_messages": chat_messages,
            "context": context_str,
            "question": question
        }
        prompt = self.prompt.format_messages(**prompt_data)
        prompt_str = self._messages_to_string(prompt)

        retrieved_docs = []
        for doc, score in documents:
            retrieved_docs.append(
                RetrievedDoc(
                    id=doc.id,
                    chat_message_id="",
                    doc_id=doc.id,
                    content=doc.page_content,
                    score=score,
                    doc_metadata=doc.metadata,
                )
            )
        return ChatMessage(
            id="",
            session_id=session_id,
            role=ChatRole.USER,
            content=user_content,
            prompt=prompt,
            prompt_str=prompt_str,
            filter_query=filter,
            retrieved_docs=retrieved_docs
        )
    
    def _messages_to_string(self, messages: list[BaseMessage]) -> str:
        """
        list[BaseMessage] を1つの文字列に連結する。
        BaseMessage.content (str or list[Union[str, dict]]) を適宜処理。
        """
        lines = []
        for i, msg in enumerate(messages, start=1):
            role = msg.type
            content = msg.content

            if isinstance(content, list):
                combined = "\n".join(str(c) for c in content)
                lines.append(f"Message {i} (role={role}):\n{combined}\n")
            else:
                lines.append(f"Message {i} (role={role}):\n{content}\n")
        return "\n".join(lines)

    
    def _build_chat_messages(self, past_messages: List[ChatMessage]) -> str:
        """
        過去のメッセージをプロンプトに変換
        """
        history = ChatMessageHistory()
        for message in past_messages:
            if message.role == "user":
                history.add_message(HumanMessage(message.content))
            elif message.role == "assistant":
                history.add_message(AIMessage(message.content))
            else:
                history.add_message(SystemMessage(message.content))
        return history
    
    def _build_context(self, documents: List[RetrievedDoc]) -> str:
        """
        metadata, content を文字列に整形して返す。
        例:
        [Doc 1]
        doc_id=abc123
        score=0.88
        metadata={'category':'foo'}
        content=Lorem ipsum ...
        
        [Doc 2]
        doc_id=def456
        score=0.77
        ...
        """
        lines = []
        for i, doc in enumerate(documents, start=1):
            lines.append(f"[Doc {i}]")
            lines.append(f"metadata={doc.doc_metadata}")
            lines.append(f"content=\n{doc.content}")
            lines.append("")

        return "\n".join(lines)


    def _build_filter(self, filter_params: Optional[FilterParams]) -> dict:
        """
        filterをdictに変換
        # TODO
        https://docs.pinecone.io/guides/data/understanding-metadata
        """
    
    def _search_pinecone(self, user_content: str, filter: dict) -> List[Tuple[Document, float]]:
        """
        pinecone検索 score付き
        """
        results = self.vector_store.similarity_search_with_score(
            query=user_content,
            k=5,
            filter=filter
        )
        return results