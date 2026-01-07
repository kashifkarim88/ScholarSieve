import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from core.config import CUE_PHRASES

# Load spaCy model with bootstrapping
def load_nlp():
    try:
        return spacy.load("en_core_web_sm", disable=["ner"])
    except:
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm", disable=["ner"])

nlp = load_nlp()

class InsightRanker:
    def score_sentences(self, section_text, section_type):
        doc = nlp(section_text)
        
        # 1. Structural Filtering: Must have a verb (Action) and sufficient length
        candidate_sentences = []
        for sent in doc.sents:
            text = sent.text.strip()
            # Ensure it contains a verb and isn't just a list of nouns/numbers
            has_verb = any(token.pos_ == "VERB" for token in sent)
            if has_verb and len(text) > 45:
                candidate_sentences.append(text)
        
        if not candidate_sentences:
            return []

        # 2. Statistical Scoring (TF-IDF)
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform(candidate_sentences)
            tfidf_scores = np.asarray(tfidf_matrix.sum(axis=1)).flatten()
        except:
            tfidf_scores = np.zeros(len(candidate_sentences))

        ranked = []
        for i, sent in enumerate(candidate_sentences):
            score = tfidf_scores[i]
            
            # 3. Cue Phrase Boosting from config
            for phrase in CUE_PHRASES.get(section_type, []):
                if phrase.lower() in sent.lower():
                    score += 3.0
            
            # 4. Section-Specific Noise Penalty
            # If in methodology, penalize sentences heavy on performance metrics
            if section_type == "methodology":
                metrics = ["acc", "ppl", "mse", "mae", "accuracy", "transformer++"]
                if any(m in sent.lower() for m in metrics):
                    score -= 5.0

            ranked.append((score, sent))
            
        return sorted(ranked, key=lambda x: x[0], reverse=True)