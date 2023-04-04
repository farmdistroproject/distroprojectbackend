from config.database import Base
from sqlalchemy import Column, Integer, String,Time,DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4,unique=True)
    user = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    balance = Column(Integer)
    amount_added = Column(Integer)
    status = Column(String(50))
    channel = Column(String(200))
    gateway_response = Column(String(200))
    created_at = Column(DateTime,default=datetime.utcnow)
    paid_at= Column(DateTime,default=datetime.utcnow)
    
