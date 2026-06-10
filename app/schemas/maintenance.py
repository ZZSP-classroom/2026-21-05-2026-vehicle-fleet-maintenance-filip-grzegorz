from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from app.models.maintenance import ServiceType


class ServiceLogBase(BaseModel):
    service_type: ServiceType
    description: str = Field(..., max_length=512)
    mileage_km: float = Field(..., ge=0)
    service_date: date
    cost: Optional[float] = Field(None, ge=0)
    technician: Optional[str] = Field(None, max_length=128)
    next_service_km: Optional[float] = Field(None, ge=0)
    next_service_date: Optional[date] = None


class ServiceLogCreate(ServiceLogBase):
    vehicle_id: int


class ServiceLogUpdate(BaseModel):
    description: Optional[str] = None
    cost: Optional[float] = None
    technician: Optional[str] = None
    next_service_km: Optional[float] = None
    next_service_date: Optional[date] = None


class ServiceLogRead(ServiceLogBase):
    id: int
    vehicle_id: int

    model_config = {"from_attributes": True}


class MaintenanceDueAlert(BaseModel):
    vehicle_id: int
    vin: str
    make: str
    model: str
    last_service_date: Optional[date]
    next_service_date: Optional[date]
    last_mileage_km: Optional[float]
    next_service_km: Optional[float]
    reason: str
