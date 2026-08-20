from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/equipment", tags=["Equipment"])

@router.post("", response_model = schemas.EquipmentOut)
def create_equipment(equipment: schemas.EquipmentCreate,db: Session = Depends(get_db)):
    new_equipment = models.Equipment(**equipment.dict())
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment

@router.get("", response_model = list[schemas.EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(models.Equipment).all()

@router.get("/{equipment_id}", response_model=schemas.EquipmentOut)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.put("/{equipment_id}", response_model = schemas.EquipmentOut)
def update_equipment(equipment_id: int, updated: schemas.EquipmentUpdate, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).fitler(models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code = 404, detail="Equipment not found")

    equipment.name = updated.name
    equipment.category = updated.category
    equipment.description = updated.description

    db.commit()
    db.refresh(equipment)
    return equipment
