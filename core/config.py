# Regex for section headers
SECTION_PATTERNS = {
    "abstract": r'(?i)\bAbstract\b',
    "introduction": r'(?i)\b(Introduction|Background)\b',
    "methodology": r'(?i)\b(Methodology|Methods|Experimental Setup|Proposed Approach)\b',
    "results": r'(?i)\b(Results|Evaluation|Findings)\b',
    "conclusion": r'(?i)\b(Conclusion|Concluding Remarks)\b',
    "limitations": r'(?i)\b(Limitations|Future Work|Discussion)\b'
}

# Signal phrases for scoring
CUE_PHRASES = {
    "contribution": ["we propose", "we present", "this paper contributes", "our method", "novel approach"],
    "methodology": ["we implemented", "using the", "algorithm", "data was collected", "framework"],
    "results": ["significant increase", "outperforms", "results show", "observed that", "accuracy of"],
    "limitations": ["however", "future work", "limitation", "restricted to", "does not address"]
}