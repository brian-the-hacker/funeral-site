from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from routers import auth, contact, gallery

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Makueni Pamoja Funeral Home API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(gallery.router)
app.include_router(contact.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
