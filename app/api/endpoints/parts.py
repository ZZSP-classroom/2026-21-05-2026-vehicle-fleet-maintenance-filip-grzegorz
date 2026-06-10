from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.schemas.parts import PartCreate, PartUpdate, PartRead
from app.crud import parts as crud

router = APIRouter(prefix="/parts", tags=["Parts & Inventory"])


@router.get("/", response_model=List[PartRead])
def list_parts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_parts(db, skip=skip, limit=limit)


@router.get("/compatible", response_model=List[PartRead])
def get_compatible_parts(
    make: str = Query(..., description="Vehicle make, e.g. 'Porsche'"),
    model: str = Query(..., description="Vehicle model, e.g. '911'"),
    db: Session = Depends(get_db),
):
    return crud.get_parts_for_vehicle(db, make, model)


@router.post("/", response_model=PartRead, status_code=status.HTTP_201_CREATED)
def create_part(data: PartCreate, db: Session = Depends(get_db)):
    if crud.get_part_by_number(db, data.part_number):
        raise HTTPException(status_code=400, detail=f"Part number '{data.part_number}' already exists.")
    return crud.create_part(db, data)


@router.get("/{part_id}", response_model=PartRead)
def get_part(part_id: int, db: Session = Depends(get_db)):
    part = crud.get_part(db, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found.")
    return part


@router.patch("/{part_id}", response_model=PartRead)
def update_part(part_id: int, data: PartUpdate, db: Session = Depends(get_db)):
    part = crud.update_part(db, part_id, data)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found.")
    return part


@router.delete("/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_part(part_id: int, db: Session = Depends(get_db)):
    if not crud.delete_part(db, part_id):
        raise HTTPException(status_code=404, detail="Part not found.")
