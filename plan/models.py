from sqlalchemy import Boolean, Column, Integer, String, DateTime
import uuid
from datetime import datetime
from config.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Plans(Base):

    __tablename__ = "plans"

    pkid = Column(Integer,primary_key=True)
    id = Column(UUID(as_uuid=True), default=uuid.uuid4,unique=True)
    name = Column(String(150))
    description = Column(String)
    duration = Column(Integer)
    price = Column(Integer)
    create_at = Column(DateTime, default=datetime.utcnow)

