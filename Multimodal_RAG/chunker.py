import spacy
from .Config import Config

class Chunker:
    def __init__(self, model=Config.SPACY_MODEL):
        try:
            self.nlp = spacy.load(model)
        except:
            # Fallback if load fails directly
            import en_core_web_sm
            self.nlp = en_core_web_sm.load()
            
        self.min_tokens = Config.MIN_TOKENS
        self.max_tokens = Config.MAX_TOKENS
        self.hard_limit = Config.HARD_LIMIT

    def chunk_text(self, text_blocks):
        """
        Chunks text blocks into segments.
        text_blocks: list of {'text': str, 'bbox': ...}
        Returns list of {'text': str, 'bbox': ..., 'chunk_id': ...}
        """
        chunks = []
        current_chunk_text = ""
        current_chunk_bbox = None
        
        for block in text_blocks:
            text = block['text']
            bbox = block['bbox']
            
            # Check if adding this block exceeds max tokens
            temp_text = current_chunk_text + " " + text if current_chunk_text else text
            
            # Optimization: Estimate token count first to avoid running nlp on every concatenation
            # 1 token approx 4 chars. 
            estimated_tokens = len(temp_text) / 4
            if estimated_tokens > self.hard_limit:
                 # Definitely too long, treat as exceeding max_tokens
                 token_count = estimated_tokens # Approximate
            else:
                doc = self.nlp(temp_text)
                token_count = len(doc)
            
            if token_count > self.max_tokens:
                # Finalize current chunk
                if current_chunk_text:
                    chunks.append({
                        'text': current_chunk_text,
                        'bbox': current_chunk_bbox, 
                        'token_count': len(self.nlp(current_chunk_text)) if len(current_chunk_text) / 4 <= self.hard_limit else len(current_chunk_text) / 4
                    })
                
                # Start new chunk
                current_chunk_text = text
                current_chunk_bbox = bbox
            else:
                current_chunk_text = temp_text
                if current_chunk_bbox is None:
                    current_chunk_bbox = bbox
                else:
                    # Union bbox
                    current_chunk_bbox = (
                        min(current_chunk_bbox[0], bbox[0]),
                        min(current_chunk_bbox[1], bbox[1]),
                        max(current_chunk_bbox[2], bbox[2]),
                        max(current_chunk_bbox[3], bbox[3])
                    )
                
        # Add last chunk
        if current_chunk_text:
            chunks.append({
                'text': current_chunk_text,
                'bbox': current_chunk_bbox,
                'token_count': len(self.nlp(current_chunk_text))
            })
            
        return chunks
