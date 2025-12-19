import fitz  # PyMuPDF
import os
from PIL import Image
import io
from .Config import Config
import datetime

class ImageExtractor:
    def __init__(self, output_dir=Config.EXTRACTED_IMAGES_DIR):
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
                
                if width < Config.MIN_IMAGE_WIDTH or height < Config.MIN_IMAGE_HEIGHT:
                    print(f"Skipping image {img_index} on page {page_no} due to size {width}x{height}")
                    continue
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"img_page{page_no}_{img_index}_{timestamp}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                # Save as PNG
                image.save(filepath, Config.IMAGE_FORMAT)
                print(f"Saved image: {filepath}")
                
                # Get bbox for all occurrences of this image on the page
                rects = page.get_image_rects(xref)
                if rects:
                    for i, rect in enumerate(rects):
                        extracted_images.append({
                            'filename': filename,
                            'bbox': list(rect),
                            'width': width,
                            'height': height,
                            'occurrence': i + 1
                        })
                else:
                    # Fallback if no rect found (unlikely if get_images returned it)
                    extracted_images.append({
                        'filename': filename,
                        'bbox': [0, 0, 0, 0],
                        'width': width,
                        'height': height,
                        'occurrence': 1
                    })
            except Exception as e:
                print(f"Error processing image {img_index} on page {page_no}: {e}")
                
        return extracted_images
