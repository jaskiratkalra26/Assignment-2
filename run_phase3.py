from phase3.main import DocumentProcessor
import os

def test():
    processor = DocumentProcessor()
    input_pdf = r"c:\Users\jaski\Downloads\attention_is_all_you_need.pdf"
    output_json = "output_attention.json"
    
    if os.path.exists(input_pdf):
        print(f"Processing {input_pdf}...")
        processor.process_pdf(input_pdf, output_json)
    else:
        print(f"File not found: {input_pdf}")

if __name__ == "__main__":
    test()
