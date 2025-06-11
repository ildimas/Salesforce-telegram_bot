from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, ForeignKey, Integer, CheckConstraint
import uuid

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    company_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String, nullable=False, unique=True)
    company_sf_id = Column(String, nullable=False, unique=True)
    company_hashed_password = Column(String, nullable=False)
    company_corporate_mail = Column(String, nullable=True)
    company_phone = Column(String, nullable=True)
    company_website = Column(String, nullable=True)
    company_additional_info = Column(Text, nullable=True)
    users = relationship("User", backref="company", cascade="all, delete")
    tickets = relationship("Ticket", backref="company", cascade="all, delete")

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_sf_id = Column(String, nullable=False, unique=True)
    user_name = Column(String, nullable=False)
    user_telegramm_id = Column(Integer, nullable=False, unique=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.company_id', ondelete="CASCADE"), nullable=False)
    tickets = relationship("Ticket", backref="user", cascade="all, delete")

class Ticket(Base):
    __tablename__ = "tickets"
    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_sf_id = Column(String, nullable=False, unique=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.company_id', ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    ticket_name = Column(String, nullable=False)
