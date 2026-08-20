from fastapi import FastAPI
from app import models, storage
from app.database import engine
from app.routers import equipment, bookings, documents

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
def root():
    return{"message": "Equipment Management API is running"}

app.include_router(equipment.router)
app.include_router(bookings.router)
app.include_router(documents.router)
