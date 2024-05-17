from sqlalchemy import Column, Integer, String, Date, ForeignKey,Float
from sqlalchemy.orm import relationship
from db import Base
# Define ListingDOA
class ListingDOA(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    begin_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    begin_date = Column(Float, nullable=False)
    status = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    capacity =  Column(Float, nullable=False)
    available_from = Column(Date, nullable=False)
    available_to = Column(Date, nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=True)

    user = relationship("UserDOA", back_populates="listing")
    booking = relationship("BookingDOA", back_populates="listing")

    def __init__(self,user_id,title,description,location,latitude,longtitude,price,capacity,available_from,available_to,created_at,updated_at,user):
        self.user_id = user_id
        self.user_id = title
        self.begin_date = description
        self.end_date = location
        self.begin_date = latitude
        self.status = longtitude
        self.price = price
        self.capacity = capacity
        self.available_from = available_from
        self.available_to = available_to
        self.created_at = created_at
        self.updated_at = updated_at
        self.user = user