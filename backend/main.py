from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from database import Base, engine
from routers import auth, contact, gallery


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if not FRONTEND_DIR.is_dir():
    raise RuntimeError(f"Frontend directory not found: {FRONTEND_DIR}")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Makueni Pamoja Funeral Home",
    description="Website and API for Makueni Pamoja Funeral Home",
    version="1.0.0",
)

# Retain CORS configuration for any future separate frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router)
app.include_router(gallery.router)
app.include_router(contact.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Public website pages
@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
def homepage():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/about", include_in_schema=False)
@app.get("/about.html", include_in_schema=False)
def about():
    return FileResponse(FRONTEND_DIR / "about.html")


@app.get("/services", include_in_schema=False)
@app.get("/services.html", include_in_schema=False)
def services():
    return FileResponse(FRONTEND_DIR / "services.html")


@app.get("/gallery", include_in_schema=False)
@app.get("/gallery.html", include_in_schema=False)
def gallery_page():
    return FileResponse(FRONTEND_DIR / "gallery.html")


@app.get("/contact", include_in_schema=False)
@app.get("/contact.html", include_in_schema=False)
def contact_page():
    return FileResponse(FRONTEND_DIR / "contact.html")


# Admin dashboard
@app.get("/admin", include_in_schema=False)
def admin_redirect():
    return RedirectResponse(url="/admin/", status_code=308)


@app.get("/admin/", include_in_schema=False)
@app.get("/admin/index.html", include_in_schema=False)
def admin_page():
    return FileResponse(FRONTEND_DIR / "admin" / "index.html")


# Serve all remaining frontend assets (CSS, JS, images, videos, etc.).
# This MUST remain last so it cannot intercept API or page routes.
app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend",
)
