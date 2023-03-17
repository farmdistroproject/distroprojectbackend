from sqlalchemy import Column, Integer, String,Boolean,ForeignKey,DateTime,Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from config.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255),unique=True)
    username = Column(String(255))
    password = Column(String)

    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number= Column(String(255))
    dob = Column(Date())

    email_verified=Column(Boolean, default=False)
    google_id = Column(String)





