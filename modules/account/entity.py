import uuid
from core import Base
from typing import TypeVar
from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy import Column, String, DateTime, UUID, Integer, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship

T = TypeVar('T')

class Account(Base):
    __tablename__ = 'accounts'
    accountID = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Enum('User', 'Admin', name='account_role'), default='User')
    profilePhoto = Column(String, default=None)

    reports = relationship('Report', back_populates='reporter')
