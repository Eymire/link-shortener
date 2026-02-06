from datetime import datetime

from pydantic import BaseModel, HttpUrl


class LinkAdd(BaseModel):
    url: HttpUrl


class LinkOut(BaseModel):
    url: HttpUrl
    short_code: str
    expires_at: datetime
