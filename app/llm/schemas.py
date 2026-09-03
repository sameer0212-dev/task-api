from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class BookCategory(str, Enum):
    SOFTWARE_ENGINEERING = "Software Engineering"
    NON_FICTION = "Non-Fiction"
    FICTION = "Fiction"
    SELF_HELP = "Self-Help"
    OTHER = "Other"

class EnrichRequest(BaseModel):
    title: str
    description: str

class EnrichResponse(BaseModel):
    category: BookCategory
    confidence: float = Field(ge=0.0, le=1.0)
    themes: List[str]
    one_sentence_summary: str
    quality_flags: List[str] = []