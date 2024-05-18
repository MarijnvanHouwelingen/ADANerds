from sqlalchemy import Column, Integer, String, Date, ForeignKey,Float
from sqlalchemy.orm import relationship,backref
from db import Base


# Define BookingDOA
class BookingDOA(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    begin_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String)

    # Booking relationship with listing
    listing_id = Column(Integer, ForeignKey('listings.id'), unique=True)
    listing = relationship("ListingDOA", backref=backref("bookings"))

    def __init__(self,begin_date,end_date,price,status,listing,listing_id):
        self.begin_date = begin_date
        self.end_date = end_date
        self.price = price
        self.status = status
        self.listing_id = listing_id
        self.listing = listing