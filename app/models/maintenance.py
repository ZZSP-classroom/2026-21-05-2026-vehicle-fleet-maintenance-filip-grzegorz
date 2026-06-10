from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class ServiceType(str, enum.Enum):
    oil_change = "oil_change"
    inspection = "inspection"
    repair = "repair"
    part_replacement = "part_replacement"
    other = "other"


class ServiceLog(Base):
    __tablename__ = "service_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    service_type = Column(SAEnum(ServiceType), nullable=False)
    description = Column(String(512), nullable=False)
    mileage_km = Column(Float, nullable=False)
    service_date = Column(Date, nullable=False)
    cost = Column(Float, nullable=True)
    technician = Column(String(128), nullable=True)
    next_service_km = Column(Float, nullable=True)
    next_service_date = Column(Date, nullable=True)

    vehicle = relationship("Vehicle", back_populates="service_logs")
