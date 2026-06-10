from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.maintenance import ServiceLogCreate, ServiceLogUpdate, ServiceLogRead, MaintenanceDueAlert
from app.crud import maintenance as crud
from app.crud import vehicle as vehicle_crud

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("/due", response_model=List[MaintenanceDueAlert])
def get_maintenance_due(db: Session = Depends(get_db)):
    return crud.get_maintenance_due_alerts(db)


@router.get("/", response_model=List[ServiceLogRead])
def list_service_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_service_logs(db, skip=skip, limit=limit)


@router.get("/vehicle/{vehicle_id}", response_model=List[ServiceLogRead])
def list_logs_for_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    if not vehicle_crud.get_vehicle(db, vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    return crud.get_service_logs_for_vehicle(db, vehicle_id)


@router.post("/", response_model=ServiceLogRead, status_code=status.HTTP_201_CREATED)
def create_service_log(data: ServiceLogCreate, db: Session = Depends(get_db)):
    if not vehicle_crud.get_vehicle(db, data.vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    return crud.create_service_log(db, data)


@router.get("/{log_id}", response_model=ServiceLogRead)
def get_service_log(log_id: int, db: Session = Depends(get_db)):
    log = crud.get_service_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Service log not found.")
    return log


@router.patch("/{log_id}", response_model=ServiceLogRead)
def update_service_log(log_id: int, data: ServiceLogUpdate, db: Session = Depends(get_db)):
    log = crud.update_service_log(db, log_id, data)
    if not log:
        raise HTTPException(status_code=404, detail="Service log not found.")
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_log(log_id: int, db: Session = Depends(get_db)):
    if not crud.delete_service_log(db, log_id):
        raise HTTPException(status_code=404, detail="Service log not found.")
