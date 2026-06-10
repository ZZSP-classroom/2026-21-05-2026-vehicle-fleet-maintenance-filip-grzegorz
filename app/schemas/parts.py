from pydantic import BaseModel, Field
from typing import Optional, List


class PartCompatibilityRead(BaseModel):
    vehicle_make: str
    vehicle_model: str

    model_config = {"from_attributes": True}


class PartBase(BaseModel):
    part_number: str = Field(..., max_length=64)
    name: str = Field(..., max_length=128)
    description: Optional[str] = Field(None, max_length=512)
    quantity: int = Field(0, ge=0)
    unit_price: Optional[float] = Field(None, ge=0)
    supplier: Optional[str] = Field(None, max_length=128)


class PartCreate(PartBase):
    compatible_makes_models: Optional[List[dict]] = []


class PartUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    unit_price: Optional[float] = None
    supplier: Optional[str] = None


class PartRead(PartBase):
    id: int
    compatible_models: List[PartCompatibilityRead] = []

    model_config = {"from_attributes": True}
