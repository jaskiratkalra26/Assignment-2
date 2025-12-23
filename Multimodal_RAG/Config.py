import os

class Config:
    # Paths
    # Use the absolute path of the project root, independent of where the script is run
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PDF_DIR = os.path.join(BASE_DIR, "pdf")
    OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
    EXTRACTED_CONTENT_DIR = os.path.join(OUTPUT_DIR, "Extracted_Content")
    EXTRACTED_IMAGES_DIR = os.path.join(OUTPUT_DIR, "Extracted_Images")
    EMBEDDINGS_DIR = os.path.join(OUTPUT_DIR, "Embeddings")
    
    # Directory to cache downloaded models to prevent re-downloading
    MODEL_CACHE_DIR = os.path.join(BASE_DIR, "model_cache")
    
    # Ensure cache directory exists
    os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
    
    # Image Extractor Settings
    MIN_IMAGE_WIDTH = 256
    MIN_IMAGE_HEIGHT = 256
    IMAGE_FORMAT = "PNG"
    
    # Text Extractor Settings
    HEADER_THRESHOLD = 0.05
    FOOTER_THRESHOLD = 0.95
    
    # Chunker Settings
    SPACY_MODEL = "en_core_web_sm"
    MIN_TOKENS = 256
    MAX_TOKENS = 512
    HARD_LIMIT = 768

    # Embedding & Captioning Settings
    EMBEDDING_MODEL_NAME = "openai/clip-vit-base-patch32"
    CAPTION_MODEL_NAME = "Salesforce/blip-image-captioning-base"
    BATCH_SIZE = 32
    DEVICE = "cpu"
    NORMALIZE_EMBEDDINGS = True
    # Directory to cache downloaded models to prevent re-downloading
    # MODEL_CACHE_DIR is defined above
