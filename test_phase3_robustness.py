import unittest
from unittest.mock import MagicMock, patch
from phase3.text_extractor import TextExtractor
from phase3.chunker import Chunker
from phase3.linker import Linker
from phase3.image_extractor import ImageExtractor

class TestPhase3(unittest.TestCase):

    def test_text_extractor_merge(self):
        extractor = TextExtractor()
        blocks = [
            {'text': 'Short', 'bbox': (0,0,10,10), 'block_no': 1},
            {'text': 'This is a longer block that should not be merged immediately.', 'bbox': (0,20,100,30), 'block_no': 2},
            {'text': 'Tiny', 'bbox': (0,40,10,50), 'block_no': 3},
            {'text': 'Another tiny', 'bbox': (0,60,10,70), 'block_no': 4}
        ]
        merged = extractor.merge_small_blocks(blocks)
        # 'Short' (5 chars) < 20 -> Merged with 'This is...'
        # 'Tiny' (4 chars) < 20 -> Merged with 'Another tiny'
        # 'Another tiny' (12 chars) -> Merged result 'Tiny Another tiny' (17 chars)
        # Wait, logic is: if current < 20, merge NEXT into CURRENT.
        # 1. Current='Short'. < 20. Merge 'This is...' into 'Short'.
        #    Current becomes 'Short This is...'.
        # 2. Next iteration. Current is 'Short This is...'. Len > 20.
        #    Append 'Short This is...'. Current becomes 'Tiny'.
        # 3. Next iteration. Current='Tiny'. < 20. Merge 'Another tiny' into 'Tiny'.
        #    Current becomes 'Tiny Another tiny'.
        # 4. End of loop. Append 'Tiny Another tiny'.
        
        self.assertEqual(len(merged), 2)
        self.assertTrue("Short This is" in merged[0]['text'])
        self.assertTrue("Tiny Another tiny" in merged[1]['text'])

    def test_chunker_limit(self):
        chunker = Chunker()
        # Mock nlp to return length based on spaces
        chunker.nlp = lambda text: text.split() 
        
        # Create blocks that sum up to > max_tokens (512)
        # Let's say 1 word = 1 token for this mock
        block1 = {'text': "word " * 300, 'bbox': (0,0,100,100)}
        block2 = {'text': "word " * 300, 'bbox': (0,100,100,200)}
        
        chunks = chunker.chunk_text([block1, block2])
        self.assertEqual(len(chunks), 2)
        self.assertEqual(len(chunks[0]['text'].split()), 300)
        self.assertEqual(len(chunks[1]['text'].split()), 300)

    def test_linker_overlap(self):
        linker = Linker()
        chunks = [
            {'text': 'Chunk 1', 'bbox': (0, 0, 100, 100), 'images': []}, # y: 0-100
            {'text': 'Chunk 2', 'bbox': (0, 200, 100, 300), 'images': []} # y: 200-300
        ]
        images = [
            {'filename': 'img1.png', 'bbox': (50, 10, 80, 90)}, # y: 10-90 (Inside Chunk 1)
            {'filename': 'img2.png', 'bbox': (50, 210, 80, 290)}, # y: 210-290 (Inside Chunk 2)
            {'filename': 'img3.png', 'bbox': (50, 110, 80, 190)} # y: 110-190 (Between, closer to Chunk 1 (dist 10) vs Chunk 2 (dist 10)? Center 150. Chunk1 center 50. Chunk2 center 250. Dist to 1: 100. Dist to 2: 100. Tie.)
        ]
        
        linked_chunks = linker.link_images_to_chunks(chunks, images)
        
        self.assertIn('img1.png', linked_chunks[0]['images'])
        self.assertIn('img2.png', linked_chunks[1]['images'])
        # img3 is equidistant. Logic: "If multiple candidates exist...". 
        # But here NO overlap. "Rule 4: Closest in y-distance".
        # Chunk 1 center: 50. Chunk 2 center: 250. Image 3 center: 150.
        # Dist to 1: 100. Dist to 2: 100.
        # It will pick the first one encountered with min_dist.
        # If chunks order is 1, 2. 
        # Check 1: dist 100. min_dist=100. best=Chunk 1.
        # Check 2: dist 100. not < min_dist. best remains Chunk 1.
        self.assertIn('img3.png', linked_chunks[0]['images'])

if __name__ == '__main__':
    unittest.main()
