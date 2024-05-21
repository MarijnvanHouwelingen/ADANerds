import datetime

import bcrypt
from sqlalchemy import Column, String, Integer, Boolean, DateTime
import uuid

from db import Base


class UserDAO(Base):
    """ User Model for storing user related details """
    __tablename__ = "usertable"

    # The id is the primary key for the table but auto increments so does not have to be filled in
    id = Column(String(255), primary_key=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin
