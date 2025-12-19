import json
import os
from typing import List
from tqdm import tqdm
from .embedding_engine import EmbeddingEngine
from .caption_engine import CaptionEngine
from .schema import EmbeddingData

def process_file(input_path: str, output_path: str):
    print(f"Processing {input_path} -> {output_path}")
    
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    embedding_engine = EmbeddingEngine()
    caption_engine = CaptionEngine()
    
    output_data = []

    for chunk in tqdm(data, desc="Processing chunks"):
        chunk_id = chunk.get("chunk_id")
        text = chunk.get("text", "")
        metadata = chunk.get("metadata", {})
        images = chunk.get("images", [])
        
        # 1. Text Embedding
        if text:
            text_vector = embedding_engine.get_text_embedding(text)
            text_embedding_data = EmbeddingData(
                id=chunk_id,
                vector=text_vector,
                object_type="text_embedding",
                original_text=text,
                metadata=metadata
            )
            output_data.append(text_embedding_data.to_dict())

        # 2. Image Processing
        for idx, image_info in enumerate(images):
            # Handle if image_info is string (path) or dict
            if isinstance(image_info, str):
                image_path = image_info
            elif isinstance(image_info, dict):
                image_path = image_info.get("path") or image_info.get("image_path")
            else:
                continue
                
            if not image_path:
                continue

            # Ensure path is absolute or correct relative to workspace
            # Assuming paths in JSON are relative to workspace root if not absolute
            if not os.path.isabs(image_path):
                image_path = os.path.abspath(image_path)
            
            if not os.path.exists(image_path):
                print(f"Warning: Image file not found: {image_path}")
                continue

            # Image Embedding
            image_vector = embedding_engine.get_image_embedding(image_path)
            if image_vector:
                image_embedding_id = f"{chunk_id}_image_{idx}"
                image_embedding_data = EmbeddingData(
                    id=image_embedding_id,
                    vector=image_vector,
                    object_type="image_embedding",
                    image_path=image_path,
                    metadata=metadata
                )
                output_data.append(image_embedding_data.to_dict())

            # Caption Generation & Embedding
            caption = caption_engine.generate_caption(image_path)
            if caption:
                caption_vector = embedding_engine.get_text_embedding(caption)
                caption_embedding_id = f"{chunk_id}_caption_{idx}"
                caption_embedding_data = EmbeddingData(
                    id=caption_embedding_id,
                    vector=caption_vector,
                    object_type="caption_embedding",
                    original_text=caption,
                    image_path=image_path,
                    metadata=metadata
                )
                output_data.append(caption_embedding_data.to_dict())

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)
    
    print(f"Saved {len(output_data)} embeddings to {output_path}")

if __name__ == "__main__":
    # Example usage
    pass
