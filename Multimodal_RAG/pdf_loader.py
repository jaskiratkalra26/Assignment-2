import fitz  # PyMuPDF

class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = None

    def load(self):
        try:
            self.doc = fitz.open(self.file_path)
            return self.doc
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return None
    
    def close(self):
        if self.doc:
            self.doc.close()
