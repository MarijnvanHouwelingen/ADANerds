from sqlalchemy import Column, Integer, String, ForeignKey,Float,Boolean
from sqlalchemy.orm import relationship,backref
from db import Base
from typing import Optional,Any

# Define BookingDOA
class BookingDOA(Base):
    """
    A SQLAlchemy ORM class representing a booking with attributes related to
    the booking's duration, price, status, and its relationship with a listing.

    Attributes:
        id (int): The primary key of the booking.
        begin_date (str): The beginning date of the booking.
        end_date (str): The end date of the booking.
        price (float): The price of the booking.
        status (Optional[str]): The status of the booking.
        Refund (bool): The status of the refund (True == refund, False == no refund).
        listing_id (int): The foreign key referencing the associated listing.
        listing (Any): The relationship to the associated listing.
    """
    __tablename__ = 'bookings'
    id:int = Column(Integer, primary_key=True)
    begin_date:str = Column(String, nullable=False)
    end_date:str = Column(String, nullable=False)
    price:float = Column(Float, nullable=False)
    status:Optional[str] = Column(String)
    refund:bool = Column(Boolean,nullable=False)
    # Booking relationship with listing
    listing_id:int = Column(Integer, ForeignKey('listings.id'), unique=True)
    listing: Any = relationship("ListingDOA", backref=backref("bookings"))

    def __init__(
        self,
        begin_date: str,
        end_date: str,
        price: float,
        status: Optional[str],
        refund:bool,
        listing: Any,
        listing_id: int
    ) -> None:
        self.begin_date = begin_date
        self.end_date = end_date
        self.price = price
        self.status = status
        self.refund = refund
        self.listing_id = listing_id
        self.listing = listing