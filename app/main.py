from fastapi import FastAPI
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

equipment = []
bookings = []

@app.get("/")
def root():
    return{"message": "Equipment Management API is running"}

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
def create_booking(
    id: int,
    equipment_id: int,
    researcher_name: str,
    email: str,
    booking_start_date: str,
    booking_end_date: str,
    booking_purpose: str
):
    for booking in bookings:
        if booking["equipment_id"] == equipment_id:
            if (booking_start_date <= booking["booking_end_date"]
                 and booking_end_date >= booking["booking_start_date"]):
                return {"message": "Equipment is already booked"}
    booking = {
        "id": id,
        "equipment_id": equipment_id,
        "researcher_name": researcher_name,
        "email": email,
        "booking_start_date": booking_start_date,
        "booking_end_date": booking_end_date,
        "booking_purpose": booking_purpose
    }

    bookings.append(booking)
    return booking

#Retrieve all bookings
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