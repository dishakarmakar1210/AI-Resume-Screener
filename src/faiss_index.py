# FAISS Index Module
import faiss
import numpy as np
import os

class FaissIndex:
    def __init__(self, dim: int):
        # Using inner product since we normalize vectors (cosine similarity)
        self.index = faiss.IndexFlatIP(dim)

    def add(self, vectors: np.ndarray):
        self.index.add(vectors)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        scores, indices = self.index.search(query_vector, top_k)
        return scores[0], indices[0]

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        faiss.write_index(self.index, path)

    @staticmethod
    def load(path: str):
        index = faiss.read_index(path)
        obj = FaissIndex(index.d)
        obj.index = index
        return obj
