import re

def chunk_text(text, max_words=200):
    # Clean extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split(" ")
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        if len(chunk.strip()) > 50:  # avoid tiny chunks
            chunks.append(chunk)

    return chunks
