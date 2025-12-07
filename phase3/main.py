import os
import json
import uuid
from .pdf_loader import PDFLoader
from .text_extractor import TextExtractor
from .image_extractor import ImageExtractor
from .table_extractor import TableExtractor
from .chunker import Chunker
from .linker import Linker
from .schema import ProcessedChunk, Metadata

class DocumentProcessor:
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.image_extractor = ImageExtractor()
        self.table_extractor = TableExtractor()
        self.chunker = Chunker()
        self.linker = Linker()

    def process_pdf(self, pdf_path, output_json_path):
        loader = PDFLoader(pdf_path)
        doc = loader.load()
        
        if not doc:
            print("Failed to load PDF.")
            return

        all_processed_chunks = []
        errors = []
        pdf_name = os.path.basename(pdf_path)

        for page_no, page in enumerate(doc):
            print(f"Processing page {page_no + 1}...")
            try:
                # 1. Extract Text
                text_blocks = self.text_extractor.extract_text_blocks(page)
                
                # 2. Extract Images
                images = self.image_extractor.extract_images(page, page_no + 1)
                
                # 3. Extract Tables
                tables = self.table_extractor.extract_tables(page)
                
                # 4. Chunk Text
                chunks = self.chunker.chunk_text(text_blocks)
                
                # 5. Link Images to Chunks
                chunks = self.linker.link_images_to_chunks(chunks, images)
                
                # 6. Create ProcessedChunk objects
                for i, chunk in enumerate(chunks):
                    chunk_id = str(uuid.uuid4())
                    
                    metadata = Metadata(
                        page_no=page_no + 1,
                        chunk_id=chunk_id,
                        section_hierarchy=[], # Placeholder
                        bbox=chunk['bbox'],
                        object_type='text',
                        source_pdf_name=pdf_name
                    )
                    
                    processed_chunk = ProcessedChunk(
                        chunk_id=chunk_id,
                        text=chunk['text'],
                        metadata=metadata,
                        images=chunk.get('images', []),
                        tables=[] 
                    )
                    
                    # Attach tables to the first chunk of the page
                    if tables and i == 0:
                         processed_chunk.tables = [t['data'] for t in tables]

                    all_processed_chunks.append(processed_chunk.to_dict())
            except Exception as e:
                import traceback
                error_entry = {
                    "error_type": type(e).__name__,
                    "page_no": page_no + 1,
                    "traceback": traceback.format_exc()
                }
                errors.append(error_entry)
                print(f"Error processing page {page_no + 1}: {e}")

        loader.close()
        
        # Save to JSON
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(all_processed_chunks, f, indent=4, ensure_ascii=False)
            
        if errors:
            error_json_path = output_json_path.replace('.json', '_errors.json')
            with open(error_json_path, 'w', encoding='utf-8') as f:
                json.dump(errors, f, indent=4, ensure_ascii=False)
            print(f"Errors encountered. Log saved to {error_json_path}")
            
        print(f"Processing complete. Output saved to {output_json_path}")

if __name__ == "__main__":
    # Example usage
    processor = DocumentProcessor()
    # processor.process_pdf("path/to/input.pdf", "output.json")
    print("DocumentProcessor initialized. Run process_pdf to start.")
