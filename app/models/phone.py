import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Phone(Base):
    __tablename__ = "phones"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    number = Column(String(20), nullable=False, index=True)
    citycode = Column(String(10), nullable=False)
    countrycode = Column(String(10), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    user = relationship("User", back_populates="phones")

    def __repr__(self):
        return f"<Phone {self.number} ({self.countrycode}-{self.citycode})>"
