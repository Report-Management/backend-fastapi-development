import uuid
from core import Base
from typing import TypeVar
from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy import Column, String, DateTime, UUID, Integer, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship

T = TypeVar('T')

class AccountEntity(Base):
    __tablename__ = 'accounts'
    accountID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Enum('User', 'Admin', name='account_role'), default='User')
    profilePhoto = Column(String, default=None)

    reports = relationship('Report', back_populates='reporter')
