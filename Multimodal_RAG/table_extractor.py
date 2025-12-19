import fitz  # PyMuPDF

class TableExtractor:
    def __init__(self):
        pass

    def extract_tables(self, page):
        """
        Extracts tables from a page using PyMuPDF's find_tables.
        Returns a list of dicts: {'bbox': (x0, y0, x1, y1), 'rows': int, 'cols': int, 'data': [[str]]}
        """
        tables = []
        try:
            # find_tables is available in PyMuPDF v1.23.0+
            tab_finder = page.find_tables()
            if tab_finder.tables:
                for tab in tab_finder.tables:
                    data = tab.extract()
                    bbox = tab.bbox
                    rows = len(data)
                    cols = len(data[0]) if rows > 0 else 0
                    
                    tables.append({
                        'bbox': bbox,
                        'rows': rows,
                        'cols': cols,
                        'data': data
                    })
        except Exception as e:
            print(f"Error extracting tables: {e}")
            
        return tables
