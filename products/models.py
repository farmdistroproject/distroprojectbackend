from sqlalchemy import Boolean, Column, Integer, String, DateTime
import uuid
from datetime import datetime
from config.database import Base
from sqlalchemy.dialects.postgresql import UUID


class Products(Base):
    __tablename__ = "products"
    pkid = Column(Integer,primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4,unique=True)
    name = Column(String(10))
    description = Column(String)
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)