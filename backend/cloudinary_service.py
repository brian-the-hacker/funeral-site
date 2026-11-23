import cloudinary
import cloudinary.uploader

from config import settings

cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.api_key,
    api_secret=settings.api_secret,
    secure=True,
)


def upload(file_or_url, public_id: str | None = None) -> dict:
    """Upload a file object or remote URL. Returns Cloudinary's response
    (we keep `secure_url`, `public_id`, `resource_type`)."""
    opts = {"folder": settings.folder, "resource_type": "auto"}
    if public_id:
        opts.update(public_id=public_id, overwrite=False, unique_filename=False)
    return cloudinary.uploader.upload(file_or_url, **opts)


def delete(public_id: str, resource_type: str = "image") -> None:
    cloudinary.uploader.destroy(public_id, resource_type=resource_type)
