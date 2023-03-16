from sqlalchemy import Column, Integer, String

from config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email = Column(String)