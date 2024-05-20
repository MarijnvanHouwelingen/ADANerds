from sqlalchemy import Column, Integer, DateTime,Float,Boolean
from db import Base
from typing import Optional

# Define BookingDOA
class BookingDOA(Base):
    """
    A SQLAlchemy ORM class representing a booking with attributes related to
    the booking's duration, price, status, and its relationship with a listing.

    Attributes:
        id (int): The primary key of the booking.
        begin_date (DateTime): The beginning date of the booking.
        end_date (DateTime): The end date of the booking.
        price (float): The price of the booking.
        status (Optional[int]): The status of the booking.
        Refund (bool): The status of the refund (True == refund, False == no refund).

    """
    __tablename__ = 'bookings'
    id:int = Column(Integer, primary_key=True)
    begin_date:DateTime = Column(DateTime, nullable=False)
    end_date:DateTime = Column(DateTime, nullable=False)
    price:float = Column(Float, nullable=False)
    status:Optional[int] = Column(Integer)
    refund:bool = Column(Boolean,nullable=False)


    def __init__(
        self,
        id:int,
        begin_date: DateTime,
        end_date: DateTime,
        price: float,
        status: Optional[str],
        refund:bool
    ) -> None:
        self.id = id
        self.begin_date = begin_date
        self.end_date = end_date
        self.price = price
        self.status = status
        self.refund = refund
  