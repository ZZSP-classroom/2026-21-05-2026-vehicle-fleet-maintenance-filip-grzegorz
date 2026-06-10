from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from app.models.maintenance import ServiceLog
from app.models.vehicle import Vehicle
from app.schemas.maintenance import ServiceLogCreate, ServiceLogUpdate, MaintenanceDueAlert

MILEAGE_THRESHOLD_KM = 1000
DAYS_THRESHOLD = 14


def get_service_log(db: Session, log_id: int) -> Optional[ServiceLog]:
    return db.query(ServiceLog).filter(ServiceLog.id == log_id).first()


def get_service_logs_for_vehicle(db: Session, vehicle_id: int) -> List[ServiceLog]:
    return (
        db.query(ServiceLog)
        .filter(ServiceLog.vehicle_id == vehicle_id)
        .order_by(ServiceLog.service_date.desc())
        .all()
    )


def get_all_service_logs(db: Session, skip: int = 0, limit: int = 100) -> List[ServiceLog]:
    return db.query(ServiceLog).offset(skip).limit(limit).all()


def create_service_log(db: Session, data: ServiceLogCreate) -> ServiceLog:
    log = ServiceLog(**data.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def update_service_log(db: Session, log_id: int, data: ServiceLogUpdate) -> Optional[ServiceLog]:
    log = get_service_log(db, log_id)
    if not log:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(log, field, value)
    db.commit()
    db.refresh(log)
    return log


def delete_service_log(db: Session, log_id: int) -> bool:
    log = get_service_log(db, log_id)
    if not log:
        return False
    db.delete(log)
    db.commit()
    return True


def get_maintenance_due_alerts(db: Session) -> List[MaintenanceDueAlert]:
    today = date.today()
    alerts: List[MaintenanceDueAlert] = []

    vehicles = db.query(Vehicle).filter(Vehicle.status == "active").all()

    for vehicle in vehicles:
        latest_log: Optional[ServiceLog] = (
            db.query(ServiceLog)
            .filter(ServiceLog.vehicle_id == vehicle.id)
            .order_by(ServiceLog.service_date.desc())
            .first()
        )

        reasons = []

        if latest_log:
            if latest_log.next_service_date:
                days_left = (latest_log.next_service_date - today).days
                if days_left <= DAYS_THRESHOLD:
                    reasons.append(
                        f"Next service due on {latest_log.next_service_date} "
                        f"({'overdue' if days_left < 0 else f'in {days_left} day(s)'})"
                    )

            if latest_log.next_service_km and latest_log.mileage_km:
                km_left = latest_log.next_service_km - latest_log.mileage_km
                if 0 < km_left <= MILEAGE_THRESHOLD_KM:
                    reasons.append(f"Next service in ~{km_left:.0f} km")
                elif km_left <= 0:
                    reasons.append(f"Mileage service overdue by {abs(km_left):.0f} km")
        else:
            reasons.append("No service history recorded")

        if reasons:
            alerts.append(
                MaintenanceDueAlert(
                    vehicle_id=vehicle.id,
                    vin=vehicle.vin,
                    make=vehicle.make,
                    model=vehicle.model,
                    last_service_date=latest_log.service_date if latest_log else None,
                    next_service_date=latest_log.next_service_date if latest_log else None,
                    last_mileage_km=latest_log.mileage_km if latest_log else None,
                    next_service_km=latest_log.next_service_km if latest_log else None,
                    reason="; ".join(reasons),
                )
            )

    return alerts
