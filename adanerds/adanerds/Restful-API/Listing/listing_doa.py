from sqlalchemy import Column, Integer, DateTime,Float
from db import Base
from typing import Optional
from datetime import datetime
# Define ListingDOA
class ListingDOA(Base):
    """
    A SQLAlchemy ORM class representing a listing with various attributes 
    related to the listing's availability, status, price, and capacity.

    Attributes:
        id (int): The primary key of the listing.
        begin_date (DateTime): The beginning date of the listing's availability.
        end_date (DateTime): The end date of the listing's availability.
        status (int): The status of the listing.
        price (float): The price of the listing.
        capacity (int): The capacity of the listing.
        available_from (DateTime): The date from which the listing is available.
        available_to (DateTime): The date until which the listing is available.
        created_at (DateTime): The timestamp when the listing was created.
        updated_at (Optional[DateTime]): The timestamp when the listing was last updated.
    """
    __tablename__ = 'listings'
    id: int = Column(Integer, primary_key=True)
    begin_date: str = Column(DateTime, nullable=False)
    end_date: str = Column(DateTime, nullable=False)
    status: float = Column(Integer, nullable=False)
    price: float = Column(Float, nullable=False)
    capacity: float =  Column(Integer, nullable=False)
    available_from: str = Column(DateTime, nullable=False)
    available_to: str = Column(DateTime, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False)
    updated_at: Optional[datetime] = Column(DateTime, nullable=True)


    def __init__(self,
        id:int,
        begin_date: DateTime,
        end_date: DateTime,
        status: int,
        price: float,
        capacity: int,
        available_from: DateTime,
        available_to: DateTime,
        created_at: DateTime,
        updated_at: Optional[DateTime] = None):

        self.id = id
        self.begin_date = begin_date
        self.end_date = end_date
        self.status = status
        self.price = price
        self.capacity = capacity
        self.available_from = available_from
        self.available_to = available_to
        self.created_at = created_at
        self.updated_at = updated_at
