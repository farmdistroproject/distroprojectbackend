from sqlalchemy import Column, Integer, String,Boolean,ForeignKey,DateTime,Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from config.database import Base


class User(Base):

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255))
    username = Column(String(255))
    password = Column(String)
    email_verified=Column(Boolean, default=False)
    profile = relationship('UserProfile',uselist=False, back_populates='user',cascade="all, delete-orphan")



class UserProfile(Base):
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id',ondelete='CASCADE'))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number= Column(String(255))
    dob = Column(Date())

    user = relationship('User', back_populates='profile')



