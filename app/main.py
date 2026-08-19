from datetime import date

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

equipment = []
bookings = []

@app.get("/")
def root():
    return {"message": "Equipment Management API is running"}


@app.get("/equipment")
def list_equipment():
    return {"equipment": []}

#Create equipment
@app.post("/equipment")
def list_equipment(id: int, name: str, category: str):
    item = {
        "id": id,
        "name": name,
        "category": category
    }
    equipment.append(item)
    return item

#Retrieve all equipment
@app.get("/equipment")
def list_equipment():
    return {"equipment": equipment}

#Retrieve one equipment
@app.get("/equipment/{id}")
def get_equipment(id: int):
    for item in equipment:
        if item["id"] ==id:
            return item
        return {"message": "Equipment not found"}

#Update equipment
@app.put("/equipment/{id}")
def update_equipment(id: int, name: str, category: str):
    for item in equipment:
        if item["id"] == id:
            item["name"] = name
            item["category"] = category
            return item
        return {"message": "Equipment not found"}

#Create booking
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
def list_bookings():
    return {"bookings": bookings}

#Retrieve one booking
@app.get("/bookings/{id}")
def get_booking(id: int):
    for booking in bookings:
        if booking["id"] ==id:
            return booking
        return {"message": "Booking not found"}

#Cancel/delete booking
@app.delete("/bookings/{id}")
def delete_booking(id: int):
    for booking in bookings:
        if booking["id"] == id:
            bookings.remove(booking)
            return {"message": "Booking cancelled"}
        return{"message": "Booking not found"}