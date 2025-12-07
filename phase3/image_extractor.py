import fitz  # PyMuPDF
import os
from PIL import Image
import io

class ImageExtractor:
    def __init__(self, output_dir="extracted_images"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def extract_images(self, page, page_no):
        """
        Extracts images from a page.
        Returns a list of dicts: {'filename': str, 'bbox': (x0, y0, x1, y1)}
        """
        image_list = page.get_images(full=True)
        extracted_images = []
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Load image to check dimensions
                image = Image.open(io.BytesIO(image_bytes))
                width, height = image.size
                
                if width < 256 or height < 256:
                    continue
                
                filename = f"img_page{page_no}_{img_index}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                # Save as PNG
                image.save(filepath, "PNG")
                
                # Get bbox
                rects = page.get_image_rects(xref)
                bbox = [0, 0, 0, 0]
                if rects:
                    bbox = list(rects[0]) # Use the first occurrence
                
                extracted_images.append({
                    'filename': filename,
                    'bbox': bbox,
                    'width': width,
                    'height': height
                })
            except Exception as e:
                print(f"Error processing image {img_index} on page {page_no}: {e}")
                
        return extracted_images
