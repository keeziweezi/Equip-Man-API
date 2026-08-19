from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Equipment(Base):
<<<<<<< HEAD
    _tablename_ = "equipment"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    serial_number = Column(String, unique = True)
    description = Column(String, nullable = True)

class Booking(Base):
    _tablename_ = "bookings"

    id = Column(Integer, primary_key = True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    researcher_name = Column(String, nullable = False)
    researcher_email = Column(String, nullable = False)
    start_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = False)
    purpose = Column(String, nullable = False)
    status = Column(String, default="active")

class Document(Base):
    _tablename_= "documents"

    id = Column(String, nullable = False)
    object_key = Column(String, nullable = False)
    content_type = Column(String, nullable = True)
    uploaded_at = Column(DateTime, default = datetime.utcnow)
    
=======
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    serial_number = Column(String, unique=True)
    description = Column(String, nullable=True)

class Booking(Base):
        __tablename__ = "bookings"

        id = Column(Integer, primary_key=True)
        equipment_id = Column(Integer, ForeignKey("equipment.id"))
        researcher_name = Column(String, nullable=False)
        researcher_email = Column(String, nullable=False)
        start_date = Column(Date, nullable=False)
        end_date = Column(Date, nullable=False)
        purpose = Column(String, nullable=False)
        status = Column(String, default="active")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    filename = Column(String, nullable=False)
    object_key = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
>>>>>>> 06fab174fc6b25722a03a0a8cc313224d849f195
