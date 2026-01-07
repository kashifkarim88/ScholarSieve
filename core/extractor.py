import pdfplumber
import re
from typing import Optional

class PDFExtractor:
    def __init__(self, file_path):
        """Initializes the extractor with the path to the PDF."""
        self.file_path = file_path

    def is_tabular(self, text, threshold=0.3):
        """Detects if a line is likely a table row."""
        stripped = text.strip()
        if not stripped or len(stripped) < 7:
            return True
        
        numbers_and_symbols = len(re.findall(r'[\d\.\%\-\+]', stripped))
        total_chars = len(stripped)
        
        ratio = numbers_and_symbols / total_chars
        return ratio > threshold

    def get_clean_text(self):
        """Extracts text while filtering out table noise and fixing PDF artifacts."""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                clean_lines = []
                
                for page in pdf.pages:
                    # FIX: We use layout settings to force word spacing
                    # x_tolerance: Increase this if words are merging (default is 3)
                    # y_tolerance: Keeps lines together (default is 3)
                    page_text = page.extract_text(x_tolerance=2, y_tolerance=3)
                    
                    if page_text:
                        for line in page_text.split('\n'):
                            if not self.is_tabular(line):
                                clean_lines.append(line)
        
        except Exception as e:
            raise Exception(f"Failed to open PDF with pdfplumber: {e}")

        # Combine lines
        full_text = " ".join(clean_lines)
        
        # Normalization
        full_text = re.sub(r'\s+', ' ', full_text)  # Collapse multiple spaces
        full_text = re.sub(r'-\s+', '', full_text)  # Fix word hyphenation
        
        return full_text.strip()

    def extract_with_context(self, include_metadata=False):
        """Extract text with page context and specific layout fixes."""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                pages_data = []
                total_pages = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    # FIX: Using layout parameters here as well
                    page_text = page.extract_text(x_tolerance=2)
                    
                    if page_text:
                        clean_lines = []
                        for line in page_text.split('\n'):
                            if not self.is_tabular(line):
                                clean_lines.append(line)
                        
                        clean_text = " ".join(clean_lines)
                        clean_text = re.sub(r'\s+', ' ', clean_text)
                        clean_text = re.sub(r'-\s+', '', clean_text)
                        
                        page_data = {
                            'page_number': page_num + 1,
                            'text': clean_text.strip()
                        }
                        
                        if include_metadata:
                            page_data.update({
                                'width': page.width,
                                'height': page.height,
                                'rotation': page.rotation
                            })
                        
                        pages_data.append(page_data)
                
                return {
                    'total_pages': total_pages,
                    'pages': pages_data
                }
                
        except Exception as e:
            raise Exception(f"Failed to extract PDF with context: {e}")

    # ... keep get_text_with_tables and from_uploaded_file the same ...