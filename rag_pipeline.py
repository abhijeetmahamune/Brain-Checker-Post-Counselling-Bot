from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

model = SentenceTransformer("all-MiniLM-L6-v2")


class RAGPipeline:
    def __init__(self):
        self.chunks = []
        self.index = None

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
            "COUNSELOR’S REMARK"
        ]

        pattern = "|".join(section_headers)
        sections = re.split(f"({pattern})", text)

        self.chunks = []
        current_chunk = ""

        for part in sections:
            if part in section_headers:
                if current_chunk:
                    self.chunks.append(current_chunk.strip())
                current_chunk = part
            else:
                current_chunk += " " + part

        if current_chunk:
            self.chunks.append(current_chunk.strip())

    def create_embeddings(self):
        embeddings = model.encode(self.chunks)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def retrieve(self, question: str):
        question_embedding = model.encode([question])
        D, I = self.index.search(np.array(question_embedding), k=1)

        return self.chunks[I[0][0]]
