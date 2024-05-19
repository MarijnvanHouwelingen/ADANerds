from sqlalchemy import Column, Integer, String, DateTime,Float
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
        begin_date (str): The beginning date of the listing's availability.
        end_date (str): The end date of the listing's availability.
        status (float): The status of the listing.
        price (float): The price of the listing.
        capacity (float): The capacity of the listing.
        available_from (str): The date from which the listing is available.
        available_to (str): The date until which the listing is available.
        created_at (datetime): The timestamp when the listing was created.
        updated_at (Optional[datetime]): The timestamp when the listing was last updated.
    """
    __tablename__ = 'listings'
    id: int = Column(Integer, primary_key=True)
    begin_date: str = Column(String, nullable=False)
    end_date: str = Column(String, nullable=False)
    status: float = Column(Float, nullable=False)
    price: float = Column(Float, nullable=False)
    capacity: float =  Column(Float, nullable=False)
    available_from: str = Column(String, nullable=False)
    available_to: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False)
    updated_at: Optional[datetime] = Column(DateTime, nullable=True)


    def __init__(self,
        begin_date: str,
        end_date: str,
        status: float,
        price: float,
        capacity: float,
        available_from: str,
        available_to: str,
        created_at: datetime,
        updated_at: Optional[datetime] = None):

        self.begin_date = begin_date
        self.end_date = end_date
        self.status = status
        self.price = price
        self.capacity = capacity
        self.available_from = available_from
        self.available_to = available_to
        self.created_at = created_at
        self.updated_at = updated_at
