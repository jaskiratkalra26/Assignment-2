from phase3.main import DocumentProcessor
import os

def test():
    processor = DocumentProcessor()
    pdf_dir = os.path.join(os.getcwd(), "pdf")
    
    if not os.path.exists(pdf_dir):
        print(f"PDF directory not found: {pdf_dir}")
        return

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the pdf directory.")
        return

    for pdf_file in pdf_files:
        input_pdf = os.path.join(pdf_dir, pdf_file)
        output_json = f"output_{os.path.splitext(pdf_file)[0]}.json"
        
        print(f"\n{'='*50}")
        print(f"Processing {input_pdf}...")
        processor.process_pdf(input_pdf, output_json)
        print(f"{'='*50}\n")

if __name__ == "__main__":
    test()
