from sqlalchemy import Column, Integer, String,ForeignKey,Float,Boolean,DateTime
from config.database import Base
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



class Cart(Base):

    __tablename__ = "cart"
    pkid = Column(Integer,primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4,unique=True)
    user = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    amount = Column(Float)
    is_paid = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.utcnow)


class CartItems(Base):
    __tablename__ ="cart_items"
    pkid = Column(Integer,primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4,unique=True)
    user = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    checkout_id = Column(UUID(as_uuid=True), ForeignKey("cart.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    price = Column(Float)
    name = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)
