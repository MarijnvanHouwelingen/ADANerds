from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship,backref
from db import Base
from typing import Any


# Define the NotificationSettingsDAO
class NotificationSettingsDAO(Base):
    """
    A SQLAlchemy ORM class representing notification settings with attributes for
    various types of notifications.

    Attributes:
        id (int): The primary key of the notification settings.
        chat_notification (bool): Whether chat notifications are enabled.
        forum_notification (bool): Whether forum notifications are enabled.
        review_notification (bool): Whether review notifications are enabled.
        booking_notification (bool): Whether booking notifications are enabled.
    """
    __tablename__ = 'notification_settings'
    id: int = Column(Integer, primary_key=True)
    chat_notification: bool = Column(Boolean, default=False)
    forum_notification: bool = Column(Boolean, default=False)
    review_notification: bool = Column(Boolean, default=False)
    booking_notification: bool = Column(Boolean, default=False)

    def __init__(
        self,
        id:int,
        chat_notification: bool = False,
        forum_notification: bool = False,
        review_notification: bool = False,
        booking_notification: bool = False
    ) -> None:
        self.id = id
        self.date_of_birth = chat_notification
        self.gender = forum_notification
        self.phone_number = review_notification
        self.address = booking_notification

# Define the UserDOA
class UserDOA(Base):
    """
    A SQLAlchemy ORM class representing a user with various personal details and
    a relationship to notification settings.

    Attributes:
        id (int): The primary key of the user.
        user_name (str): The unique username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email_address (str): The unique email address of the user.
        password (str): The password of the user.
        notification_id (Optional[int]): The foreign key referencing the user's notification settings.
        notification_settings (Optional[NotificationSettingsDAO]): The relationship to the associated notification settings.
    """
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    user_name: str = Column(String, unique=True, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email_address: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)

    # foreign key
    notification_id: int = Column(Integer, ForeignKey("notification_settings.id"))

    # Define the relationships for the User DOA
    notification_settings = relationship(NotificationSettingsDAO.__name__, backref=backref('users',uselist=False))
    
    def __init__(
        self,
        id:int,
        user_name: str,
        first_name: str,
        last_name: str,
        email_address: str,
        password: str,
        notification_settings,
        notification_id: int 
    ) -> None:
        self.id = id
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
    """
    A SQLAlchemy ORM class representing a user profile with personal details and
    a relationship to a user.

    Attributes:
        id (int): The primary key of the profile.
        date_of_birth (date): The date of birth of the user.
        gender (str): The gender of the user.
        phone_number (str): The phone number of the user.
        address (str): The address of the user.
        user_id (Optional[int]): The foreign key referencing the associated user.
        user (Optional[UserDOA]): The relationship to the associated user.
    """
    __tablename__ = 'profiles'
    id: int = Column(Integer, primary_key=True)
    date_of_birth: Date = Column(Date, nullable=False)
    gender: str = Column(String, nullable=False)
    phone_number: str = Column(String, nullable=False)
    address: str = Column(String, nullable=False)

    # Foreign key
    user_id: int = Column(Integer, ForeignKey("users.id"))

    # Relationship for the Profile DOA
    user = relationship(UserDOA.__name__, backref = backref('profiles',uselist=False))
    
    def __init__(
        self,
        id:int,
        date_of_birth: Date,
        gender: str,
        phone_number: str,
        address: str,
        user = None,
        user_id: int = None
    ) -> None:
        self.id = id,
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_number = phone_number
        self.address = address
        self.user = user
        self.user_id = user_id





