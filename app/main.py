from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import uuid
from app import models, storage
from app.database import engine, get_db

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.on_event("startup")
def startup():
    storage.ensure_bucket()

@app.get("/")
def root():
    return {"message": "Equipment Management API is running"}

#Create equipment
@app.post("/equipment")
def create_equipment(name: str, category: str, serial_number: str, db: Session = Depends(get_db)):
    equipment = models.Equipment(name = name, category = category, serial_number = serial_number)
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment

@app.get("/equipment")
def list_equipment(db: Session = Depends(get_db)):
    return db.query(models.Equipment).all()

#Create equipment
@app.get("/equipment/{equipment_id}")
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code = 404, detail = "Equipment not found")
    return equipment

#New document end points
@app.post("/equipment/{equipment_id}/documents")
def upload_document(equipment_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    object_key = f"equipment/{equipment_id}/{uuid.uuid4()}_{file.filename}"
    storage.s3.upload_fileobj(file.file, storage.BUCKET_NAME, object_key)

    document = models.Document(
        equipment_id=equipment_id,
        filename=file.filename,
        object_key=object_key,
        content_type=file.content_type,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@app.get("/equipment/{equipment_id}/documents")
def list_documents(equipment_id: int, db: Session = Depends(get_db)):
    return db.query(models.Document).filter(models.Document.equipment_id == equipment_id).all()

@app.get("/documents/{document_id}/download")
def download_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    obj = storage.s3.get_object(Bucket=storage.BUCKET_NAME, Key=document.object_key)
    return StreamingResponse(
        obj["Body"],
        media_type=document.content_type or "application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={document.filename}"},
    )


""""
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
        return{"message": "Booking not found"}"""
