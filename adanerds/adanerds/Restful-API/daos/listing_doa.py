from sqlalchemy import Column, Integer, String, Date, ForeignKey,Float
from sqlalchemy.orm import relationship
from db import Base

# Define ListingDOA
class ListingDOA(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longtitude = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    capacity =  Column(Float, nullable=False)
    available_from = Column(Date, nullable=False)
    available_to = Column(Date, nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=True)
    user = relationship("UserDAO", back_populates="listings")

    def __init__(self,user_id,title,description,location,latitude,longtitude,price,capacity,available_from,available_to,created_at,updated_at,user):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.location = location
        self.latitude = latitude
        self.longtitude = longtitude
        self.price = price
        self.capacity = capacity
        self.available_from = available_from
        self.available_to = available_to
        self.created_at = created_at
        self.updated_at = updated_at
        self.user = user