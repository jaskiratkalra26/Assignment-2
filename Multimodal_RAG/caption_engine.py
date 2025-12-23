import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from .Config import Config

class CaptionEngine:
    def __init__(self):
        self.device = Config.DEVICE
        self.model_name = Config.CAPTION_MODEL_NAME
        print(f"Loading caption model: {self.model_name} on {self.device}...")
        
        try:
            print("Attempting to load caption model from cache...")
            self.processor = BlipProcessor.from_pretrained(self.model_name, cache_dir=Config.MODEL_CACHE_DIR, local_files_only=True)
            self.model = BlipForConditionalGeneration.from_pretrained(self.model_name, cache_dir=Config.MODEL_CACHE_DIR, local_files_only=True).to(self.device)
            print("Loaded caption model from cache.")
        except Exception as e:
            print(f"Model not found in cache or error loading: {e}. Downloading...")
            self.processor = BlipProcessor.from_pretrained(self.model_name, cache_dir=Config.MODEL_CACHE_DIR)
            self.model = BlipForConditionalGeneration.from_pretrained(self.model_name, cache_dir=Config.MODEL_CACHE_DIR).to(self.device)
            print("Downloaded and loaded caption model.")

    def generate_caption(self, image_path: str) -> str:
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                out = self.model.generate(**inputs)
            
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            print(f"Error generating caption for image {image_path}: {e}")
            return ""
