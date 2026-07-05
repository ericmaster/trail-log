import asyncio
import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
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
    """Upload a .fit file with metadata.

    Defined as an ``async def`` route: the request body is read without
    blocking via ``await file.read()``, and the blocking filesystem writes and
    database calls are offloaded to a threadpool with ``asyncio.to_thread`` so
    they never stall the event loop.
    """
    # Validate file extension
    if not file.filename.lower().endswith(".fit"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .fit files are allowed",
        )

    # Read the upload contents without blocking the event loop.
    contents = await file.read()

    # Strip any directory components to prevent path traversal (e.g. a
    # filename like "../../evil.fit" escaping the user's upload directory).
    safe_filename = os.path.basename(file.filename)

    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    saved_filename = f"{timestamp}_{safe_filename}"

    # Offload the blocking filesystem writes to a worker thread.
    user_upload_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    filepath = os.path.join(user_upload_dir, saved_filename)

    def _save_file() -> None:
        os.makedirs(user_upload_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(contents)

    await asyncio.to_thread(_save_file)

    # Create database record. The SQLAlchemy session is not thread-safe, so all
    # of its blocking calls run together in a single worker thread.
    db_upload = models.Upload(
        user_id=current_user.id,
        filename=safe_filename,
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

    def _persist_upload() -> models.Upload:
        db.add(db_upload)
        db.commit()
        db.refresh(db_upload)
        return db_upload

    return await asyncio.to_thread(_persist_upload)


@router.get("/", response_model=list[schemas.UploadResponse])
def list_uploads(
    skip: int = 0,
    limit: int = Query(20, le=100),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all uploads for the current user."""
    uploads = (
        db.query(models.Upload)
        .filter(models.Upload.user_id == current_user.id)
        .order_by(models.Upload.upload_date.desc(), models.Upload.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return uploads
