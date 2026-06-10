from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.parts import Part, PartCompatibility
from app.schemas.parts import PartCreate, PartUpdate


def get_part(db: Session, part_id: int) -> Optional[Part]:
    return db.query(Part).filter(Part.id == part_id).first()


def get_part_by_number(db: Session, part_number: str) -> Optional[Part]:
    return db.query(Part).filter(Part.part_number == part_number).first()


def get_parts(db: Session, skip: int = 0, limit: int = 100) -> List[Part]:
    return db.query(Part).offset(skip).limit(limit).all()


def get_parts_for_vehicle(db: Session, make: str, model: str) -> List[Part]:
    return (
        db.query(Part)
        .join(Part.compatible_models)
        .filter(
            PartCompatibility.vehicle_make.ilike(make),
            PartCompatibility.vehicle_model.ilike(model),
        )
        .all()
    )


def create_part(db: Session, data: PartCreate) -> Part:
    compatible = data.compatible_makes_models or []
    part_data = data.model_dump(exclude={"compatible_makes_models"})
    part = Part(**part_data)
    db.add(part)
    db.flush()

    for compat in compatible:
        db.add(PartCompatibility(
            part_id=part.id,
            vehicle_make=compat.get("vehicle_make", ""),
            vehicle_model=compat.get("vehicle_model", ""),
        ))

    db.commit()
    db.refresh(part)
    return part


def update_part(db: Session, part_id: int, data: PartUpdate) -> Optional[Part]:
    part = get_part(db, part_id)
    if not part:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(part, field, value)
    db.commit()
    db.refresh(part)
    return part


def delete_part(db: Session, part_id: int) -> bool:
    part = get_part(db, part_id)
    if not part:
        return False
    db.delete(part)
    db.commit()
    return True
