from pydantic import BaseModel
from typing import List, Optional

class ChunkModel(BaseModel):
    file_source: str
    label: str
    content: str
    page_number: Optional[int] = None
    created_at: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class UploadJSONModel(BaseModel):
    success: bool
    content_source_id: int
    chunks: List[ChunkModel] 