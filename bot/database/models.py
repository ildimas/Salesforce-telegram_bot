from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, ForeignKey, Integer, CheckConstraint
import uuid

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    company_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String, nullable=False)
    company_hashed_password = Column(String, nullable=False)
    company_corporeate_mail = Column(String, nullable=True, unique=True)
    company_phone = Column(String, nullable=True)
    company_website = Column(String, nullable=True)
    company_additional_info = Column(Text, nullable=True)
    users = relationship("User", backref="company", cascade="all, delete")
    tickets = relationship("Ticket", backref="company", cascade="all, delete")

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_phone = Column(String, nullable=True)
    user_email = Column(String, nullable=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.company_id', ondelete="CASCADE"), nullable=False)
    user_additional_info = Column(Text, nullable=True)
    tickets = relationship("Ticket", backref="user", cascade="all, delete")

class Ticket(Base):
    __tablename__ = "tickets"
    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.company_id', ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    ticket_name = Column(String, nullable=False)
    ticket_priority = Column(
        Integer, 
        CheckConstraint('ticket_priority >= 1 AND ticket_priority <= 10', name='check_ticket_priority'),
        nullable=False
    )