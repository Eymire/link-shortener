from datetime import datetime

from pydantic import BaseModel, HttpUrl


class LinkAdd(BaseModel):
    original_url: HttpUrl


class LinkOut(BaseModel):
    original_url: HttpUrl
    short_code: str
    expires_at: datetime
