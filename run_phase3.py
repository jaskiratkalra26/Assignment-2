from phase3.main import DocumentProcessor
import os

def test():
    processor = DocumentProcessor()
    input_pdf = r"c:\Users\jaski\Downloads\Phase3_Feature_Document_Detailed.pdf"
    output_json = "output_feature_doc.json"
    
    if os.path.exists(input_pdf):
        print(f"Processing {input_pdf}...")
        processor.process_pdf(input_pdf, output_json)
    else:
        print(f"File not found: {input_pdf}")

if __name__ == "__main__":
    test()
