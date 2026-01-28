from collections import defaultdict

def search_resumes(query: str, embedder, index, chunk_texts, chunk_to_resume, top_k=10):
    query_vec = embedder.encode([query])

    scores, indices = index.search(query_vec, top_k)

    resume_matches = defaultdict(list)

    for score, idx in zip(scores, indices):
        if idx == -1:
            continue

        resume_name = chunk_to_resume[idx]
        chunk_text = chunk_texts[idx]

        resume_matches[resume_name].append({
            "score": float(score),
            "chunk": chunk_text
        })

    # Aggregate per resume
    final_results = []
    for resume, matches in resume_matches.items():
        # Sort chunks by score
        matches.sort(key=lambda x: x["score"], reverse=True)

        final_results.append({
            "filename": resume,
            "score": matches[0]["score"],  # best chunk score
            "top_chunks": matches[:3]      # keep top 3 matching chunks
        })

    # Sort resumes by best score
    final_results.sort(key=lambda x: x["score"], reverse=True)

    return final_results
