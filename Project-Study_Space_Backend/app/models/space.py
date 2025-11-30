from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    func,
    ForeignKey,
    Table
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base

# ======================================================
# ASSOCIATION TABLE Space <-> Utility (ONE AND ONLY)
# ======================================================

space_utilities = Table(
    "space_utilities",
    Base.metadata,
    Column("space_id", Integer, ForeignKey("spaces.id", ondelete="CASCADE"), primary_key=True),
    Column("utility_id", Integer, ForeignKey("utilities.id", ondelete="CASCADE"), primary_key=True),
)


# ======================================================
# SPACE MODEL
# ======================================================

class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="available")
    location = Column(String, nullable=False)

    description = Column(String, nullable=True)
    equipment = Column(JSONB, nullable=True)

    average_rating = Column(Float, nullable=False, server_default="0")
    total_ratings = Column(Integer, nullable=False, server_default="0")

    is_active = Column(Boolean, nullable=False, server_default="true")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    bookings = relationship(
        "Booking",
        back_populates="space",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    ratings = relationship(
        "Rating",
        back_populates="space",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # ⭐ Correct Many-to-Many
    utilities = relationship(
        "Utility",
        secondary=space_utilities,
        back_populates="spaces",
        lazy="selectin",
    )
