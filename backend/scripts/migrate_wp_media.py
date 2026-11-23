"""Copy every photo/video from the old WordPress site into Cloudinary
and register it in the gallery table.

Run from the backend/ folder (after filling in .env):
    python -m scripts.migrate_wp_media

Safe to re-run: files already in the database are skipped.
"""
from pathlib import Path

import cloudinary_service as cdn
from database import Base, SessionLocal, engine
from models import GalleryItem

Base.metadata.create_all(bind=engine)
urls = [u.strip() for u in (Path(__file__).parent / "wp_media_urls.txt").read_text().splitlines() if u.strip()]
db = SessionLocal()
done = {i.public_id.rsplit("/", 1)[-1] for i in db.query(GalleryItem).all()}

for n, url in enumerate(urls, 1):
    stem = Path(url).stem
    if stem in done:
        print(f"[{n}/{len(urls)}] skip {stem}")
        continue
    try:
        res = cdn.upload(url, public_id=stem)
        db.add(GalleryItem(public_id=res["public_id"], url=res["secure_url"],
                           resource_type=res.get("resource_type", "image")))
        db.commit()
        print(f"[{n}/{len(urls)}] ok   {stem}")
    except Exception as e:
        db.rollback()
        print(f"[{n}/{len(urls)}] FAIL {stem}: {e}")
