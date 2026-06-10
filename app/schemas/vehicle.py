from pydantic import BaseModel, Field
from typing import Optional
from app.models.vehicle import VehicleStatus, EngineType


class VehicleBase(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17, description="Vehicle Identification Number")
    make: str = Field(..., max_length=64)
    model: str = Field(..., max_length=64)
    year: int = Field(..., ge=1886, le=2100)
    engine_type: EngineType
    engine_displacement_cc: Optional[int] = Field(None, ge=50)
    horsepower: Optional[int] = Field(None, ge=1)
    transmission: Optional[str] = Field(None, max_length=32)
    status: VehicleStatus = VehicleStatus.active
    notes: Optional[str] = Field(None, max_length=512)


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    engine_type: Optional[EngineType] = None
    engine_displacement_cc: Optional[int] = None
    horsepower: Optional[int] = None
    transmission: Optional[str] = None
    status: Optional[VehicleStatus] = None
    notes: Optional[str] = None


class VehicleRead(VehicleBase):
    id: int

    model_config = {"from_attributes": True}
