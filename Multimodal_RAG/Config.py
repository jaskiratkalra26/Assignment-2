import os

class Config:
    # Paths
    BASE_DIR = os.getcwd()
    PDF_DIR = os.path.join(BASE_DIR, "pdf")
    OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
    EXTRACTED_CONTENT_DIR = os.path.join(OUTPUT_DIR, "Extracted_Content")
    EXTRACTED_IMAGES_DIR = os.path.join(OUTPUT_DIR, "Extracted_Images")
    
    # Image Extractor Settings
    MIN_IMAGE_WIDTH = 100
    MIN_IMAGE_HEIGHT = 100
    IMAGE_FORMAT = "PNG"
    
    # Text Extractor Settings
    HEADER_THRESHOLD = 0.05
    FOOTER_THRESHOLD = 0.95
    
    # Chunker Settings
    SPACY_MODEL = "en_core_web_sm"
    MIN_TOKENS = 256
    MAX_TOKENS = 512
    HARD_LIMIT = 768
