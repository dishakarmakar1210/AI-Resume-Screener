import streamlit as st
import os

from src.embedder import Embedder
from src.faiss_index import FaissIndex
from src.search import search_resumes
from src.chunker import chunk_text
from src.pdf_loader import load_resumes_from_folder
from src.storage import save_metadata, load_metadata
from src.skill_extractor import extract_skills
from src.category_classifier import classify_resume


RESUME_FOLDER = "data/resumes"
INDEX_PATH = "index/faiss.index"
META_PATH = "index/meta.pkl"

st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("📄 AI-Powered Resume Screening System")
st.write("Upload resumes and paste a job description to find the best matching candidates using semantic search.")

# ========== Sidebar ==========
st.sidebar.header("📂 Upload Resumes")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)
rebuild = st.sidebar.button("🔁 Rebuild Index")
st.sidebar.header("🗂️ Filter by Category")

selected_category = st.sidebar.selectbox(
    "Show candidates from:",
    ["All", "Civil", "Mechanical", "Electrical", "IT / Software", "Finance", "Other"]
)


# ========== Save uploaded files ==========
if uploaded_files:
    os.makedirs(RESUME_FOLDER, exist_ok=True)

    for file in uploaded_files:
        file_path = os.path.join(RESUME_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())

    st.sidebar.success("Resumes uploaded successfully!")

# ========== Index handling ==========
def build_or_load_index():
    embedder = Embedder()

    # ===== Load existing index =====
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH) and not rebuild:
        st.info("Loading existing FAISS index...")

        index = FaissIndex.load(INDEX_PATH)
        meta = load_metadata(META_PATH)

        all_chunks = meta["all_chunks"]
        chunk_to_resume = meta["chunk_to_resume"]
        resume_to_skills = meta["resume_to_skills"]
        resume_to_category = meta["resume_to_category"]


        return embedder, index, all_chunks, chunk_to_resume, resume_to_skills, resume_to_category

    # ===== Rebuild index =====
    st.warning("Building new index from resumes...")

    resume_texts, filenames = load_resumes_from_folder(RESUME_FOLDER)

    if len(resume_texts) == 0:
        st.error("No resumes found. Please upload PDFs.")
        return None, None, None, None, None

    # ===== Chunking =====
    all_chunks = []
    chunk_to_resume = []

    for text, fname in zip(resume_texts, filenames):
        chunks = chunk_text(text)
        for ch in chunks:
            all_chunks.append(ch)
            chunk_to_resume.append(fname)

    st.write(f"Total chunks: {len(all_chunks)}")

    # ===== Skill extraction =====
    resume_to_skills = {}
    for text, fname in zip(resume_texts, filenames):
        resume_to_skills[fname] = extract_skills(text)
    
    # ===== Category classification =====
    resume_to_category = {}
    for text, fname in zip(resume_texts, filenames):
        resume_to_category[fname] = classify_resume(text)


    # ===== Embeddings =====
    st.info("Generating embeddings...")
    embeddings = embedder.encode(all_chunks)

    dim = embeddings.shape[1]

    # ===== Build FAISS =====
    st.info("Building FAISS index...")
    index = FaissIndex(dim)
    index.add(embeddings)

    # ===== Save =====
    os.makedirs("index", exist_ok=True)
    index.save(INDEX_PATH)
    save_metadata(
        {
            "all_chunks": all_chunks,
            "chunk_to_resume": chunk_to_resume,
            "resume_to_skills": resume_to_skills,
            "resume_to_category": resume_to_category
        },
        META_PATH
    )

    st.success("Index built and saved!")

    return embedder, index, all_chunks, chunk_to_resume, resume_to_skills, resume_to_category

# ========== Main UI ==========
st.subheader("📝 Paste Job Description")

job_description = st.text_area(
    "Enter the job description here:",
    height=200,
    placeholder="e.g. Looking for a GenAI / ML engineer with Python, NLP, Transformers, RAG experience..."
)

search_button = st.button("🔍 Find Best Candidates")

if search_button:
    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        embedder, index, all_chunks, chunk_to_resume, resume_to_skills, resume_to_category = build_or_load_index()

        if index is not None:
            st.subheader("🏆 Top Matching Resumes")

            results = search_resumes(
                job_description,
                embedder,
                index,
                all_chunks,
                chunk_to_resume,
                top_k=20
            )

            # ===== Apply category filter =====
            if selected_category != "All":
                results = [
                    r for r in results
                    if resume_to_category.get(r["filename"], "Other") == selected_category
                    ]


            if len(results) == 0:
                st.warning("No matching resumes found.")
            else:
                # 🔥 EVERYTHING IS INSIDE THE LOOP 🔥
                for i, res in enumerate(results[:5], 1):
                    st.markdown(f"## {i}. 📄 {res['filename']}")
                    st.markdown(f"**Similarity Score:** `{res['score']:.4f}`")

                    category = resume_to_category.get(res["filename"], "Other")
                    st.markdown(f"**Category:** `{category}`")

                    # ===== Skills =====
                    skills = resume_to_skills.get(res["filename"], [])

                    if skills:
                        st.markdown("**Extracted Skills:**")
                        st.write(", ".join(skills))
                    else:
                        st.markdown("_No skills detected from skill list._")

                    # ===== Matching Sections =====
                    st.markdown("**Top Matching Sections:**")

                    for j, chunk_info in enumerate(res["top_chunks"], 1):
                        with st.expander(f"Match {j} (score: {chunk_info['score']:.4f})"):
                            st.write(chunk_info["chunk"])

                    st.markdown("---")



