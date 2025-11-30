# app/models/utility.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship
from app.models.space import space_utilities

class Utility(Base):
    __tablename__ = "utilities"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), nullable=False, unique=True, index=True)
    label = Column(String(100), nullable=False)
    description = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Utility id={self.id} key={self.key}>"
    
    spaces = relationship(
    "Space",
    secondary= space_utilities,
    back_populates="utilities",
)
