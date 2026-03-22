import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RAGPipeline:
    def __init__(self):
        self.chunks = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.matrix = None

    def chunk_text(self, text: str):
        section_headers = [
            "STUDENT DETAILS",
            "BRAIN CHECKER PSYCHOMETRIC TEST",
            "IQ SCORE",
            "PARAMETER WISE SCORE CARD",
            "12 PARAMETERS AT A GLANCE",
            "Holland Theory",
            "Holland's RIASEC Theory",
            "Carl Jung Personality Score",
            "COUNSELOR'S REMARK"
        ]

        pattern = "|".join(re.escape(h) for h in section_headers)
        sections = re.split(f"({pattern})", text)

        self.chunks = []
        current_chunk = ""

        for part in sections:
            if part in section_headers:
                if current_chunk.strip():
                    self.chunks.append(current_chunk.strip())
                current_chunk = part
            else:
                current_chunk += " " + part

        if current_chunk.strip():
            self.chunks.append(current_chunk.strip())

    def create_embeddings(self):
        self.matrix = self.vectorizer.fit_transform(self.chunks)

    def retrieve(self, question: str, k: int = 2) -> str:
        question_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(question_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:k]
        return "\n\n".join(self.chunks[i] for i in top_indices)