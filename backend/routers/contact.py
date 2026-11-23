import smtplib
from email.message import EmailMessage

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from auth import require_admin
from config import settings
from database import get_db
from models import ContactMessage
from schemas import ContactIn, ContactOut

router = APIRouter(prefix="/api/contact", tags=["contact"])


def _notify(m: ContactMessage):
    if not (settings.smtp_host and settings.notify_to):
        return
    msg = EmailMessage()
    msg["Subject"] = f"Website enquiry: {m.subject}"
    msg["From"] = settings.smtp_user or settings.notify_to
    msg["To"] = settings.notify_to
    msg["Reply-To"] = m.email
    msg.set_content(f"From: {m.name} <{m.email}>\nPhone: {m.phone}\n\n{m.message}")
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as s:
            s.starttls()
            if settings.smtp_user:
                s.login(settings.smtp_user, settings.smtp_password)
            s.send_message(msg)
    except Exception as e:  # the message is already saved; don't fail the visitor
        print("Email notification failed:", e)


@router.post("", status_code=201)
def send_message(data: ContactIn, bg: BackgroundTasks, db: Session = Depends(get_db)):
    if data.website:  # honeypot filled in: pretend success, store nothing
        return {"ok": True}
    m = ContactMessage(**data.model_dump(exclude={"website"}))
    db.add(m)
    db.commit()
    db.refresh(m)
    bg.add_task(_notify, m)
    return {"ok": True}


@router.get("", response_model=list[ContactOut], dependencies=[Depends(require_admin)])
def list_messages(db: Session = Depends(get_db)):
    return db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).limit(200).all()


@router.patch("/{msg_id}/handled", dependencies=[Depends(require_admin)])
def mark_handled(msg_id: int, db: Session = Depends(get_db)):
    m = db.get(ContactMessage, msg_id)
    if m:
        m.handled = True
        db.commit()
    return {"ok": True}
