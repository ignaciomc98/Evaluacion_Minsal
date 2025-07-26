import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    password = Column(String(255), nullable=False)
    
    token = Column(String(500), nullable=False)

    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, default=datetime.utcnow, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    phones = relationship(
        "Phone",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined" 
    )

    def __repr__(self):
        return f"<User email={self.email} active={self.is_active}>"
