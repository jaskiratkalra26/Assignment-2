import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch.nn.functional as F
from .config import Config

class EmbeddingEngine:
    def __init__(self):
        self.device = Config.DEVICE
        self.model_name = Config.EMBEDDING_MODEL_NAME
        print(f"Loading embedding model: {self.model_name} on {self.device}...")
        self.model = CLIPModel.from_pretrained(self.model_name, cache_dir=Config.MODEL_CACHE_DIR).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.model_name, cache_dir=Config.MODEL_CACHE_DIR)
        self.normalize = Config.NORMALIZE_EMBEDDINGS

    def get_text_embedding(self, text: str):
        inputs = self.processor(text=[text], return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model.get_text_features(**inputs)
        
        embedding = outputs[0]
        if self.normalize:
            embedding = F.normalize(embedding, p=2, dim=0)
            
        return embedding.cpu().tolist()

    def get_image_embedding(self, image_path: str):
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.get_image_features(**inputs)
            
            embedding = outputs[0]
            if self.normalize:
                embedding = F.normalize(embedding, p=2, dim=0)
                
            return embedding.cpu().tolist()
        except Exception as e:
            print(f"Error generating embedding for image {image_path}: {e}")
            return None
