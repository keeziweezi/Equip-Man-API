from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("", response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    if booking.end_date < booking.start_date:
        raise HTTPException(status_code=400, detail="End date cannot be before start date")

    equipment = db.query(models.Equipment).filter(models.Equipment.id == booking.equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    clash = db.query(models.Booking).filter(models.Booking.equipment_id == booking.equipment_id,
    models.Booking.status == "active",
    models.Booking.start_date <= booking.end_date,
    models.Booking.end_date >= booking.start_date,).first()
    if clash:
        raise HTTPException(status_code=409, detail="Equipment is already booked for those dates")

    new_booking = models.Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("", response_model=list[schemas.BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = "cancelled"
    db.commit()
    return {"message": "Booking cancelled"}

