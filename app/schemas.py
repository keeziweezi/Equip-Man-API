from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

#Equipment
class EquipmentCreate(BaseModel):
    name: str
    category: str
    serial_number: str
    description: Optional[str] = None

class EquipmentUpdate (BaseModel):
    name: str
    category: str
    description: Optional[str] = None

class EquipmentOut (BaseModel):
    id: int
    name: str
    category: str
    serial_number: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

#Booking
class BookingCreate(BaseModel):
    equipment_id: int
    researcher_name: str
    researcher_email: EmailStr
    start_date: date
    end_date: date
    purpose: str

class BookingOut(BaseModel):
    id: int
    equipment_id: int
    researcher_name: str
    researcher_email: str
    start_date: date
    end_date: date
    purpose: str
    status: str

    class Config:
        from_attributes = True

#Document
class DocumentOut(BaseModel):
    id: int
    equipment: int
    filename: str
    content_type: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True