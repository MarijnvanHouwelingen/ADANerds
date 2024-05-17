from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship,backref
from db import Base
from daos.listing_doa import ListingDOA
from daos.booking_doa import BookingDOA

# Define the NotificationSettingsDAO
class NotificationSettingsDAO(Base):
    __tablename__ = 'notification_settings'
    id = Column(Integer, primary_key=True)
    chat_notification = Column(Boolean, default=False)
    forum_notification = Column(Boolean, default=False)
    review_notification = Column(Boolean, default=False)
    booking_notification = Column(Boolean, default=False)

    def __init__(self,chat_notification,forum_notification,review_notification,booking_notification):
        self.date_of_birth = chat_notification
        self.gender = forum_notification
        self.phone_number = review_notification
        self.address = booking_notification

# Define the UserDOA
class UserDOA(Base):
    """
    Class doc string
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email_address = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # foreign key
    notification_id = Column(Integer, ForeignKey("notification_settings.id"))

    # Define the relationships for the User DOA
    notification_settings = relationship(NotificationSettingsDAO.__name__, backref=backref('users',uselist=False))
    
    listing = relationship(ListingDOA.__name__, back_populates="user")
    booking = relationship(BookingDOA.__name__, back_populates="user")

    def __init__(self,user_name,first_name,last_name,email_address,password,notification_settings,notification_id):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password

        # Relationship User and notification_settings
        self.notification_settings = notification_settings
        self.notification_id = notification_id

# Define the ProfileDAO
class ProfileDAO(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship for the Profile DOA
    user = relationship(UserDOA.__name__, backref = backref('profiles',uselist=False))
    
    def __init__(self,date_of_birth,gender,phone_number,address,user,user_id):
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_number = phone_number
        self.address = address
        self.user = user
        self.user_id = user_id





