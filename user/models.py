from sqlalchemy import Column, Integer, String,Boolean,DateTime,Date
from config.database import Base
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    id = Column(String(36), primary_key=True,default=str(uuid.uuid4())) #string to make it unique
    email = Column(String(255),unique=True)
    password = Column(String)

    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number= Column(Integer)
    date_of_birth = Column(Date())
    date_registered = Column(DateTime, default=datetime.utcnow)

    email_verified=Column(Boolean, default=False)
    google_id = Column(String)





