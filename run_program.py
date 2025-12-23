from Multimodal_RAG.main import DocumentProcessor
from Multimodal_RAG.embedding_processor import process_file
from Multimodal_RAG.Config import Config
import os
import datetime

def test():
    # Define output directories from Config
    output_base_dir = Config.OUTPUT_DIR
    content_dir = Config.EXTRACTED_CONTENT_DIR
    images_dir = Config.EXTRACTED_IMAGES_DIR
    embeddings_dir = Config.EMBEDDINGS_DIR
    
    # Create directories if they don't exist
    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(embeddings_dir, exist_ok=True)

    processor = DocumentProcessor(image_output_dir=images_dir)
    pdf_dir = Config.PDF_DIR
    
    if not os.path.exists(pdf_dir):
        print(f"PDF directory not found: {pdf_dir}")
        return

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the pdf directory.")
        return

    for pdf_file in pdf_files:
        input_pdf = os.path.join(pdf_dir, pdf_file)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_json = os.path.join(content_dir, f"output_{os.path.splitext(pdf_file)[0]}_{timestamp}.json")
        
        print(f"\n{'='*50}")
        print(f"Processing {input_pdf}...")
        processor.process_pdf(input_pdf, output_json)
        
        print(f"Generating embeddings for {output_json}...")
        embedding_output_json = os.path.join(embeddings_dir, f"embeddings_{os.path.splitext(pdf_file)[0]}_{timestamp}.json")
        process_file(output_json, embedding_output_json)
        
        print(f"{'='*50}\n")

if __name__ == "__main__":
    test()
