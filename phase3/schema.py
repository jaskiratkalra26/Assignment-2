from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Metadata:
    page_no: int
    chunk_id: str
    section_hierarchy: List[str]
    bbox: List[float]  # [x0, y0, x1, y1]
    object_type: str  # 'text', 'image', 'table'
    source_pdf_name: str
    caption: Optional[str] = None

@dataclass
class ProcessedChunk:
    chunk_id: str
    text: str
    metadata: Metadata
    images: List[str] = field(default_factory=list)  # List of image filenames
    tables: List[Dict[str, Any]] = field(default_factory=list) # List of table data

    def to_dict(self):
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "metadata": self.metadata.__dict__,
            "images": self.images,
            "tables": self.tables
        }
