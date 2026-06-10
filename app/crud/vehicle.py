from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def get_vehicle(db: Session, vehicle_id: int) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def get_vehicle_by_vin(db: Session, vin: str) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.vin == vin).first()


def get_vehicles(db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
    return db.query(Vehicle).offset(skip).limit(limit).all()


def create_vehicle(db: Session, data: VehicleCreate) -> Vehicle:
    vehicle = Vehicle(**data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update_vehicle(db: Session, vehicle_id: int, data: VehicleUpdate) -> Optional[Vehicle]:
    vehicle = get_vehicle(db, vehicle_id)
    if not vehicle:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(vehicle, field, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_vehicle(db: Session, vehicle_id: int) -> bool:
    vehicle = get_vehicle(db, vehicle_id)
    if not vehicle:
        return False
    db.delete(vehicle)
    db.commit()
    return True
