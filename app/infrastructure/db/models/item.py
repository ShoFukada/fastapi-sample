from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.db.session import Base

class ItemORM(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    discount_rate = Column(Float)