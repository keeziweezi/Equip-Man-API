from datetime import date

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Equipment Management API is running"}


# ---------- EQUIPMENT ----------

@app.post("/equipment")
def create_equipment(name: str, category: str, serial_number: str,
                     db: Session = Depends(get_db)):
    equipment = models.Equipment(name=name, category=category,
                                 serial_number=serial_number)
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@app.get("/equipment")
def list_equipment(db: Session = Depends(get_db)):
    return db.query(models.Equipment).all()


@app.get("/equipment/{equipment_id}")
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(
        models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@app.put("/equipment/{equipment_id}")
def update_equipment(equipment_id: int, name: str, category: str,
                     db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(
        models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    equipment.name = name
    equipment.category = category
    db.commit()
    db.refresh(equipment)
    return equipment


# ---------- BOOKINGS ----------

@app.post("/bookings")
def create_booking(equipment_id: int, researcher_name: str,
                   researcher_email: str, start_date: date,
                   end_date: date, purpose: str,
                   db: Session = Depends(get_db)):

    if end_date < start_date:
        raise HTTPException(status_code=400,
                            detail="End date cannot be before start date")

    equipment = db.query(models.Equipment).filter(
        models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    clash = db.query(models.Booking).filter(
        models.Booking.equipment_id == equipment_id,
        models.Booking.status == "active",
        models.Booking.start_date <= end_date,
        models.Booking.end_date >= start_date,
    ).first()
    if clash:
        raise HTTPException(status_code=409,
                            detail="Equipment is already booked for those dates")

    booking = models.Booking(
        equipment_id=equipment_id,
        researcher_name=researcher_name,
        researcher_email=researcher_email,
        start_date=start_date,
        end_date=end_date,
        purpose=purpose,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@app.get("/bookings")
def list_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()


@app.get("/bookings/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = "cancelled"
    db.commit()
    return {"message": "Booking cancelled"}