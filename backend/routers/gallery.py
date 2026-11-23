from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

import cloudinary_service as cdn
from auth import require_admin
from database import get_db
from models import GalleryItem
from schemas import GalleryOut

router = APIRouter(prefix="/api/gallery", tags=["gallery"])
MAX_BYTES = 40 * 1024 * 1024
ALLOWED = ("image/", "video/")


@router.get("", response_model=list[GalleryOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(GalleryItem).order_by(GalleryItem.created_at.desc()).all()


@router.post("", response_model=GalleryOut, dependencies=[Depends(require_admin)])
async def add_item(
    file: UploadFile = File(...),
    caption: str = Form(""),
    db: Session = Depends(get_db),
):
    if not (file.content_type or "").startswith(ALLOWED):
        raise HTTPException(400, "Only photos and videos can be uploaded.")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(400, "File is larger than 40 MB. Compress it and try again.")
    res = cdn.upload(data)
    item = GalleryItem(
        public_id=res["public_id"],
        url=res["secure_url"],
        resource_type=res.get("resource_type", "image"),
        caption=caption[:200],
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(GalleryItem, item_id)
    if not item:
        raise HTTPException(404, "Item not found.")
    cdn.delete(item.public_id, item.resource_type)
    db.delete(item)
    db.commit()
