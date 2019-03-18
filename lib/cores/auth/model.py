#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime as dt
import uuid

from cells.tools.werkzeug_security import (
    check_password_hash, generate_password_hash
)
from celorm.utils import Model
from sqlalchemy import (
    BOOLEAN, Column, DateTime, SMALLINT, VARCHAR
)


__prefix__ = "sys_"


class User(Model):
    __tablename__ = __prefix__ + "users"

    _id = Column(VARCHAR(36), primary_key=True)
    email = Column(VARCHAR(100), unique=True, index=True)
    username = Column(VARCHAR(20), unique=True, index=True)
    password = Column(VARCHAR(50))
    user_level = Column(SMALLINT, default=0)
    is_confirmed = Column(BOOLEAN, default=False)

    add_date = Column(DateTime)
    last_login = Column(DateTime, nullable=True)

    def __init__(self, username, password, email):
        self.add_date = dt.datetime.today()
        self._id = str(uuid.uuid4())

        self.username = username
        self.password = self.set_password(password)
        self.email = email

    @property
    def id(self):
        return self._id

    @staticmethod
    def set_password(password):
        return generate_password_hash(password, method="md5", salt_length=6)  # pw_hash

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.username)
