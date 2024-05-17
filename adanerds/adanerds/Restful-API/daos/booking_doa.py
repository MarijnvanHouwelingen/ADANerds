from sqlalchemy import Column, Integer, String, Date, ForeignKey,Float
from sqlalchemy.orm import relationship
from db import Base


# Define BookingDOA
class BookingDOA(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    begin_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String)

    user = relationship("UserDOA", back_populates="booking")
    listing = relationship("ListingDOA", back_populates='booking')

    def __init__(self,listing_id,user_id,begin_date,end_date,price,status,user,listing):
        self.listing_id = listing_id
        self.user_id = user_id
        self.begin_date = begin_date
        self.end_date = end_date
        self.price = price
        self.status = status
        self.user = user
        self.listing = listing