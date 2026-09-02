from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field

class RawBookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str

class ValidatedBookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_gbp: float = Field(..., ge=0.0)
    price_text: str
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: datetime