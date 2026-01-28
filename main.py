# Resume Screening MLOps Main Entry Point
from src.pdf_loader import load_resumes_from_folder
from src.embedder import Embedder
from src.faiss_index import FaissIndex
from src.search import search_resumes
from src.chunker import chunk_text
from src.storage import save_metadata, load_metadata
import os

RESUME_FOLDER = "data/resumes"
INDEX_PATH = "index/faiss.index"
META_PATH = "index/meta.pkl"

def main():
    print("Creating embedder...")
    embedder = Embedder()

    # ========== LOAD OR BUILD INDEX ==========
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        print("Loading existing FAISS index and metadata...")

        index = FaissIndex.load(INDEX_PATH)
        meta = load_metadata(META_PATH)

        all_chunks = meta["all_chunks"]
        chunk_to_resume = meta["chunk_to_resume"]
        resume_to_skills = meta["resume_to_skills"]

    else:
        print("No index found. Building new index from resumes...")

        print("Loading resumes...")
        resume_texts, filenames = load_resumes_from_folder(RESUME_FOLDER)
        print(f"Loaded {len(resume_texts)} resumes")

        print("Chunking resumes...")
        all_chunks = []
        chunk_to_resume = []

        for text, fname in zip(resume_texts, filenames):
            chunks = chunk_text(text)
            for ch in chunks:
                all_chunks.append(ch)
                chunk_to_resume.append(fname)

        print("Total chunks:", len(all_chunks))

        print("Generating embeddings...")
        embeddings = embedder.encode(all_chunks)

        dim = embeddings.shape[1]
        print(f"Embedding dimension: {dim}")

        print("Building FAISS index...")
        index = FaissIndex(dim)
        index.add(embeddings)

        print("Saving index and metadata...")
        from src.skill_extractor import extract_skills

        # Build resume -> skills map
        resume_to_skills = {}

        for text, fname in zip(resume_texts, filenames):
            skills = extract_skills(text)
            resume_to_skills[fname] = skills

        save_metadata(
        {
            "all_chunks": all_chunks,
            "chunk_to_resume": chunk_to_resume,
            "resume_to_skills": resume_to_skills
        },
        META_PATH)

    print("System ready!")

    # ========== SEARCH LOOP ==========
    while True:
        print("\nEnter job description (or type 'exit'):")
        query = input("> ")

        if query.lower() == "exit":
            break

        results = search_resumes(
            query,
            embedder,
            index,
            all_chunks,
            chunk_to_resume,
            top_k=15
        )

        print("\nTop Matches:\n")
        for i, res in enumerate(results[:5], 1):
            print(f"{i}. {res['filename']}  | Score: {res['score']:.4f}")

if __name__ == "__main__":
    main()
