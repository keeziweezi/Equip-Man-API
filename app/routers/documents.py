from fastapi import APIRouter, Depends, HTTPException, UploadFile, File 
from fastapi.responses import StreamingResponse 
from sqlalchemy.orm import Session 
import uuid 
from app import models, storage 
from app.database import get_db

router = APIRouter(tags=["Documents"])

@router.post("/equipment/{equipment_id}/documents")
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
        content_type=file.content_type
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

@router.get("/equipment/{equipment_id}/documents")
def list_documents(equipment_id: int, db: Session = Depends(get_db)):
    return db.query(models.Document).filter(models.Document.equipment_id == equipment_id).all()

@router.get("/documents/{document_id}/download")
def download_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    ojb = storage.s3.get_object(Bucket=storage.BUCKET_NAME, Key=document.object_key)
    return StreamingResponse(
        ojb['Body'], 
        media_type=document.content_type or "application/octet-stream", 
        headers={"Content-Disposition": f"attachment; filename={document.filename}"}
        )