import fitz  # PyMuPDF
import re

class TextExtractor:
    def __init__(self):
        pass

    def extract_text_blocks(self, page):
        """
        Extracts text blocks from a page.
        Returns a list of dicts: {'text': str, 'bbox': (x0, y0, x1, y1)}
        """
        blocks = page.get_text("blocks")
        cleaned_blocks = []
        
        page_height = page.rect.height
        
        # Heuristic for header/footer: top 5% and bottom 5% of the page
        header_thresh = page_height * 0.05
        footer_thresh = page_height * 0.95

        for b in blocks:
            # b is (x0, y0, x1, y1, "text", block_no, block_type)
            if len(b) < 7:
                continue
            x0, y0, x1, y1, text, block_no, block_type = b
            
            # Filter out headers and footers
            if y1 < header_thresh or y0 > footer_thresh:
                continue
                
            text = self.clean_text(text)
            if not text:
                continue
                
            cleaned_blocks.append({
                'text': text,
                'bbox': (x0, y0, x1, y1),
                'block_no': block_no
            })
            
        # Merge small blocks
        merged_blocks = self.merge_small_blocks(cleaned_blocks)
        return merged_blocks

    def clean_text(self, text):
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Normalize unicode (basic)
        text = text.replace('\u2013', '-').replace('\u2014', '-')
        return text

    def merge_small_blocks(self, blocks):
        if not blocks:
            return []
            
        merged = []
        current_block = blocks[0]
        
        for next_block in blocks[1:]:
            if len(current_block['text']) < 20:
                # Merge with next block
                # Update bbox to encompass both
                new_bbox = (
                    min(current_block['bbox'][0], next_block['bbox'][0]),
                    min(current_block['bbox'][1], next_block['bbox'][1]),
                    max(current_block['bbox'][2], next_block['bbox'][2]),
                    max(current_block['bbox'][3], next_block['bbox'][3])
                )
                current_block['text'] += " " + next_block['text']
                current_block['bbox'] = new_bbox
            else:
                merged.append(current_block)
                current_block = next_block
        
        merged.append(current_block)
        return merged
