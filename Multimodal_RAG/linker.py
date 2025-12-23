class Linker:
    def __init__(self):
        pass

    def link_images_to_chunks(self, chunks, images):
        """
        Links images to the most relevant text chunks based on proximity.
        chunks: list of dicts with 'bbox'
        images: list of dicts with 'bbox'
        """
        if not chunks:
            return chunks
        
        # Initialize images list for each chunk
        for chunk in chunks:
            chunk['images'] = []

        if not images:
            return chunks

        for img in images:
            best_chunk = None
            min_dist = float('inf')
            
            img_bbox = img['bbox']
            # Use vertical center for distance
            img_y_center = (img_bbox[1] + img_bbox[3]) / 2
            
            for chunk in chunks:
                chunk_bbox = chunk['bbox']
                if not chunk_bbox:
                    continue
                    
                chunk_y_center = (chunk_bbox[1] + chunk_bbox[3]) / 2
                
                # Simple vertical distance between centers
                dist = abs(img_y_center - chunk_y_center)
                
                if dist < min_dist:
                    min_dist = dist
                    best_chunk = chunk
            
            if best_chunk:
                best_chunk['images'].append(img['filename'])
                
        return chunks
