from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class VehicleStatus(str, enum.Enum):
    active = "active"
    in_shop = "in_shop"
    decommissioned = "decommissioned"


class EngineType(str, enum.Enum):
    petrol = "petrol"
    diesel = "diesel"
    electric = "electric"
    hybrid = "hybrid"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String(17), unique=True, nullable=False, index=True)
    make = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    year = Column(Integer, nullable=False)
    engine_type = Column(SAEnum(EngineType), nullable=False)
    engine_displacement_cc = Column(Integer, nullable=True)
    horsepower = Column(Integer, nullable=True)
    transmission = Column(String(32), nullable=True)
    status = Column(SAEnum(VehicleStatus), default=VehicleStatus.active, nullable=False)
    notes = Column(String(512), nullable=True)

    service_logs = relationship("ServiceLog", back_populates="vehicle", cascade="all, delete-orphan")
