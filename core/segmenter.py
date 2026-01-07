import re
from core.config import SECTION_PATTERNS

class SectionSegmenter:
    def segment(self, text):
        sections = {k: "" for k in SECTION_PATTERNS.keys()}
        found_markers = []
        
        for section, pattern in SECTION_PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                found_markers.append((match.start(), section))
        
        found_markers.sort()
        for i in range(len(found_markers)):
            start_idx, section_name = found_markers[i]
            end_idx = found_markers[i+1][0] if i+1 < len(found_markers) else len(text)
            sections[section_name] = text[start_idx:end_idx].strip()
            
        return sections