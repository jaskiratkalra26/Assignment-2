import os

class Config:
    EMBEDDING_MODEL_NAME = "openai/clip-vit-base-patch32"
    CAPTION_MODEL_NAME = "Salesforce/blip-image-captioning-base"
    BATCH_SIZE = 32
    DEVICE = "cpu"
    NORMALIZE_EMBEDDINGS = True
    # Directory to cache downloaded models to prevent re-downloading
    MODEL_CACHE_DIR = os.path.join(os.getcwd(), "model_cache")
