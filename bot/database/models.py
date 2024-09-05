from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import uuid

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    company_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

