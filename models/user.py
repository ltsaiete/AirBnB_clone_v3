#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from models import storage_t
import hashlib
from sqlalchemy import Column, String, event
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)


if storage_t == 'db':
    @event.listens_for(User, 'before_insert')
    @event.listens_for(User, 'before_update')
    def hash_password(mapper, connection, target):
        p = target.password
        target.password = hashlib.md5(p.encode('utf8')).hexdigest()
