class Linker:
    def __init__(self):
        pass

    def link_images_to_chunks(self, chunks, images):
        """
        Links images to chunks based on spatial rules.
        chunks: list of chunk dicts
        images: list of image dicts
        """
        # Reset images in chunks
        for chunk in chunks:
            if 'images' not in chunk:
                chunk['images'] = []

        for img in images:
            img_bbox = img['bbox']
            img_y_center = (img_bbox[1] + img_bbox[3]) / 2
            
            best_chunk = None
            min_dist = float('inf')
            
            # Rule 1: Vertical overlap
            overlapping_chunks = []
            for chunk in chunks:
                chunk_bbox = chunk['bbox']
                if not chunk_bbox: continue
                
                # Check vertical overlap
                # Overlap if not (above or below)
                if not (chunk_bbox[3] < img_bbox[1] or chunk_bbox[1] > img_bbox[3]):
                    overlapping_chunks.append(chunk)
            
            if overlapping_chunks:
                # If multiple, choose closest
                for chunk in overlapping_chunks:
                    chunk_y_center = (chunk['bbox'][1] + chunk['bbox'][3]) / 2
                    dist = abs(chunk_y_center - img_y_center)
                    if dist < min_dist:
                        min_dist = dist
                        best_chunk = chunk
            else:
                # Rule 4: Closest in y-distance
                for chunk in chunks:
                    chunk_bbox = chunk['bbox']
                    if not chunk_bbox: continue
                    
                    chunk_y_center = (chunk['bbox'][1] + chunk['bbox'][3]) / 2
                    dist = abs(chunk_y_center - img_y_center)
                    if dist < min_dist:
                        min_dist = dist
                        best_chunk = chunk
            
            if best_chunk:
                best_chunk['images'].append(img['filename'])
                
        return chunks
