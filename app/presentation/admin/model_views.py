from sqladmin import Admin, ModelView
from app.infrastructure.db.models.item import ItemORM

class ItemModelView(ModelView, model=ItemORM):
    column_list = [column.name for column in ItemORM.__table__.columns]