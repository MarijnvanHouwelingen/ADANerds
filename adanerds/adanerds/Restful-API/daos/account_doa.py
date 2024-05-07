from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

# Define the UserDAO
class UserDAO(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email_address = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self,user_name,first_name,last_name,email_address,password):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password

# Define the ProfileDAO
class ProfileDAO(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    user = relationship("UserDAO", back_populates="profile")
    
    def __init__(self,user_id,date_of_birth,gender,phone_number,address,user):
        self.user_id = user_id
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_number = phone_number
        self.address = address
        self.user = user

# Define the NotificationSettingsDAO
class NotificationSettingsDAO(Base):
    __tablename__ = 'notification_settings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    chat_notification = Column(Boolean, default=False)
    forum_notification = Column(Boolean, default=False)
    review_notification = Column(Boolean, default=False)
    booking_notification = Column(Boolean, default=False)
    user = relationship("UserDAO", back_populates="notification_settings")

    def __init__(self,user_id,chat_notification,forum_notification,review_notification,booking_notification,user):
        self.user_id = user_id
        self.date_of_birth = chat_notification
        self.gender = forum_notification
        self.phone_number = review_notification
        self.address = booking_notification
        self.user = user

UserDAO.profile = relationship("ProfileDAO", uselist=False, back_populates="user")
UserDAO.notification_settings = relationship("NotificationSettingsDAO", uselist=False, back_populates="user")


