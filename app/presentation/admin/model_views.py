from sqladmin import Admin, ModelView
from app.infrastructure.db.models import ItemORM, UserORM, ChatSessionORM, ChatMessageORM, RetrievedDocORM

class ItemModelView(ModelView, model=ItemORM):
    column_list = [column.name for column in ItemORM.__table__.columns]

class UserModelView(ModelView, model=UserORM):
    column_list = [column.name for column in UserORM.__table__.columns]

class ChatSessionModelView(ModelView, model=ChatSessionORM):
    column_list = [column.name for column in ChatSessionORM.__table__.columns]

class ChatMessageModelView(ModelView, model=ChatMessageORM):
    column_list = [column.name for column in ChatMessageORM.__table__.columns]

class RetrievedDocModelView(ModelView, model=RetrievedDocORM):
    column_list = [column.name for column in RetrievedDocORM.__table__.columns]