import fitz
import re

class PDFExtractor:
    def __init__(self, file_path):
        """Initializes the extractor with the path to the PDF."""
        self.file_path = file_path

    def is_tabular(self, text, threshold=0.3):
        """
        Detects if a line is likely a table row.
        Logic: If more than 30% of the characters are digits or symbols, 
        it's likely a table/metric row, not a sentence.
        """
        stripped = text.strip()
        if not stripped or len(stripped) < 7:
            return True
        
        # Count digits and special characters (., %, etc)
        numbers_and_symbols = len(re.findall(r'[\d\.\%\-\+]', stripped))
        total_chars = len(stripped)
        
        ratio = numbers_and_symbols / total_chars
        return ratio > threshold

    def get_clean_text(self):
        """Extracts text while filtering out table noise and fixing PDF artifacts."""
        try:
            doc = fitz.open(self.file_path)
        except Exception as e:
            raise Exception(f"Failed to open PDF: {e}")

        clean_lines = []
        for page in doc:
            page_text = page.get_text("text")
            for line in page_text.split('\n'):
                # Denoising: Only keep lines that are NOT tabular
                if not self.is_tabular(line):
                    clean_lines.append(line)
        
        full_text = " ".join(clean_lines)
        
        # Normalization: Collapse whitespace and fix hyphenation
        full_text = re.sub(r'\s+', ' ', full_text)
        full_text = re.sub(r'-\s+', '', full_text)
        return full_text.strip()