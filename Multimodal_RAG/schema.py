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

@dataclass
class EmbeddingData:
    id: str
    vector: List[float]
    object_type: str # 'text_embedding', 'image_embedding', 'caption_embedding'
    original_text: Optional[str] = None
    image_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "vector": self.vector,
            "object_type": self.object_type,
            "original_text": self.original_text,
            "image_path": self.image_path,
            "metadata": self.metadata
        }
