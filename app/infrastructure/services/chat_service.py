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
from app.core.config import settings


class ChatMessageService(ChatMessageServiceInterface):
    def __init__(self):
        self.pinecone = Pinecone(
            api_key=settings.PINECONE_API_KEY,
        )
        index = self.pinecone.Index(settings.PINECONE_INDEX_NAME)
        api = settings.PINECONE_INDEX_NAME
        embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL_NAME, api_key=settings.OPENAI_API_KEY)
        self.vector_store = PineconeVectorStore(index, embeddings)
        self.model = ChatOpenAI(
            model=settings.OPENAI_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
        )
        self.streaming_model = ChatOpenAI(
            model=settings.OPENAI_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            streaming=True,
        )
        self.system_prompt = settings.OPENAI_SYSTEM_PROMPT
        self.user_prompt = settings.OPENAI_USER_PROMPT
        self.prompt = ChatPromptTemplate(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_messages"),
                ("user", self.user_prompt),
            ]
        )

    def generate_answer(self, user_message: ChatMessage) -> str:
        answer = self.model.invoke(user_message.prompt)
        return answer.content
    
    def generate_answer_stream(self, user_message: ChatMessage) -> Generator[str, None, None]:
        stream = self.streaming_model.stream(user_message.prompt)
        for chunk in stream:
            yield chunk.content
            
    
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
                    doc_id=doc.id,
                    content=doc.page_content,
                    score=score,
                    doc_metadata=doc.metadata,
                )
            )
        return ChatMessage(
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

    
    def _build_chat_messages(self, past_messages: List[ChatMessage]) -> List[BaseMessage]:
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
        return history.messages
    
    def _build_context(
        self,
        documents_with_scores: List[Tuple[Document, float]]
    ) -> str:
        """
        similarity_search_with_score から返却される (Document, float) のタプルリストを受け取り、
        メタデータやテキストを1つの文字列に整形して返す。
        
        例:
        [Doc 1]
        metadata={'category': 'foo'}
        content=
        Lorem ipsum ...
        score=0.88

        [Doc 2]
        ...
        """
        lines = []
        for i, (doc, score) in enumerate(documents_with_scores, start=1):
            lines.append(f"[Doc {i}]")
            lines.append(f"metadata={doc.metadata}")        # doc.metadata でOK
            lines.append(f"content=\n{doc.page_content}")
            lines.append(f"score={score}")
            lines.append("")  # 空行

        return "\n".join(lines)



    def _build_filter(self, filter_params: Optional[FilterParams]) -> dict:
        """
        FilterParams から Pinecone 用のフィルタ dict を生成する。
        例:
            {
                "created_at": {
                    "$gte": "2023-01-01T00:00:00",
                    "$lte": "2023-02-01T00:00:00"
                },
                "prefecture": {"$eq": "Tokyo"},
                "location": {"$eq": "Shibuya"}
            }
        """

        # フィルタが指定されていない or 全て None なら空 dict を返す
        if not filter_params:
            return {}

        filter_dict = {}

        # 日付範囲フィルタ
        if filter_params.created_at_start or filter_params.created_at_end:
            created_at_filter = {}
            if filter_params.created_at_start:
                created_at_filter["$gte"] = filter_params.created_at_start.isoformat()
            if filter_params.created_at_end:
                created_at_filter["$lte"] = filter_params.created_at_end.isoformat()
            filter_dict["created_at"] = created_at_filter

        # 都道府県フィルタ（完全一致）
        if filter_params.prefecture:
            filter_dict["prefecture"] = {"$eq": filter_params.prefecture}

        # 場所フィルタ（完全一致）
        if filter_params.location:
            filter_dict["location"] = {"$eq": filter_params.location}

        return filter_dict


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