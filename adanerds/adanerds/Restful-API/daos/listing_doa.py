from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Float
from sqlalchemy.orm import relationship
from db import Base
# Define ListingDOA
class ListingDOA(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    begin_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    status = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    capacity =  Column(Float, nullable=False)
    available_from = Column(String, nullable=False)
    available_to = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)


    def __init__(self,begin_date,end_date,status,price,capacity,available_from,available_to,created_at,updated_at):
        self.begin_date = begin_date
        self.end_date = end_date
        self.status = status
        self.price = price
        self.capacity = capacity
        self.available_from = available_from
        self.available_to = available_to
        self.created_at = created_at
        self.updated_at = updated_at
