import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/api/upload", tags=["uploads"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/data/uploads")


@router.post("/", response_model=schemas.UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_fit_file(
    file: UploadFile = File(...),
    session_type: Optional[str] = Form(None),
    race_name: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    fatigue_level: Optional[int] = Form(None),
    general_sensation: Optional[int] = Form(None),
    sleep_quality: Optional[int] = Form(None),
    hydration_status: Optional[str] = Form(None),
    weather_condition: Optional[str] = Form(None),
    trail_condition: Optional[str] = Form(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a .fit file with metadata."""
    # Validate file extension
    if not file.filename.lower().endswith(".fit"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .fit files are allowed",
        )

    # Create user directory if it doesn't exist
    user_upload_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_upload_dir, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    saved_filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(user_upload_dir, saved_filename)

    # Save file
    contents = await file.read()
    with open(filepath, "wb") as f:
        f.write(contents)

    # Create database record
    db_upload = models.Upload(
        user_id=current_user.id,
        filename=file.filename,
        filepath=filepath,
        session_type=session_type,
        race_name=race_name,
        notes=notes,
        fatigue_level=fatigue_level,
        general_sensation=general_sensation,
        sleep_quality=sleep_quality,
        hydration_status=hydration_status,
        weather_condition=weather_condition,
        trail_condition=trail_condition,
    )
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)

    return db_upload


@router.get("/", response_model=list[schemas.UploadResponse])
def list_uploads(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all uploads for the current user."""
    uploads = db.query(models.Upload).filter(models.Upload.user_id == current_user.id).all()
    return uploads
