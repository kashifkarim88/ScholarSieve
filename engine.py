from core.extractor import PDFExtractor
from core.segmenter import SectionSegmenter
from core.ranker import InsightRanker

class ResearchInsightEngine:
    def __init__(self, pdf_path):
        self.extractor = PDFExtractor(pdf_path)
        self.segmenter = SectionSegmenter()
        self.ranker = InsightRanker()

    def get_insights(self, top_n=3):
        text = self.extractor.get_clean_text()
        sections = self.segmenter.segment(text)
        
        results = {
            "title": self.extractor.file_path.split('/')[-1],
            "contribution": self._get_sec_insights(sections, "introduction", "contribution", top_n),
            "methodology": self._get_sec_insights(sections, "methodology", "methodology", top_n),
            "results": self._get_sec_insights(sections, "results", "results", top_n),
            "limitations": self._get_sec_insights(sections, "limitations", "limitations", top_n)
        }
        return results

    def _get_sec_insights(self, sections, sec_key, cue_key, top_n):
        if not sections[sec_key]: return []
        scored = self.ranker.score_sentences(sections[sec_key], cue_key)
        return [s[1] for s in scored[:top_n]]