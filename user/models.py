from sqlalchemy import Column, Integer, String,Boolean,DateTime,Date
from config.database import Base
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID




class User(Base):

    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True) #string to make it unique
    email = Column(String(255),unique=True)
    password = Column(String)

    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number= Column(Integer)
    date_of_birth = Column(Date())
    date_registered = Column(DateTime, default=datetime.utcnow)

    email_verified=Column(Boolean, default=False)
    google_id = Column(String)






