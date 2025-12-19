from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

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
