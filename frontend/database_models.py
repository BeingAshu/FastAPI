from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String)
    age = Column(String)
