from sqlalchemy import Column, Integer, String,FLOAT
from database import Base

# Define To Do class inheriting from Base
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    country = Column(String(256))
    city = Column(String(256))
    location = Column(String(256))
    zip_code = Column(Integer)
    latitude = Column(String(500))
    longitude = Column(String(500))