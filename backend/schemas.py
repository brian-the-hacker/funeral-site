from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GalleryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    resource_type: str
    caption: str


class ContactIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(default="", max_length=40)
    subject: str = Field(min_length=2, max_length=200)
    message: str = Field(default="", max_length=3000)
    website: str = ""  # honeypot: real visitors leave this empty


class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    phone: str
    subject: str
    message: str
    handled: bool
    created_at: datetime
