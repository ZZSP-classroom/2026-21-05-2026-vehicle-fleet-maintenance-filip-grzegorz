from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


part_vehicle_compatibility = Table(
    "part_vehicle_compatibility",
    Base.metadata,
    Column("part_id", Integer, ForeignKey("parts.id"), primary_key=True),
    Column("vehicle_model", String(128), primary_key=True),
)


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(String(512), nullable=True)
    quantity = Column(Integer, default=0, nullable=False)
    unit_price = Column(Float, nullable=True)
    supplier = Column(String(128), nullable=True)

    compatible_models = relationship(
        "PartCompatibility",
        back_populates="part",
        cascade="all, delete-orphan",
    )


class PartCompatibility(Base):
    __tablename__ = "part_compatibility"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)
    vehicle_make = Column(String(64), nullable=False)
    vehicle_model = Column(String(64), nullable=False)

    part = relationship("Part", back_populates="compatible_models")
