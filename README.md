# 📄 AI-Powered Resume Intelligence & Screening System

An end-to-end **AI-driven resume screening and candidate intelligence system** that helps recruiters automatically **categorize, search, and rank resumes** using semantic search and Natural Language Processing (NLP).

This project is designed to **save hours of manual screening work** by using Transformer-based embeddings and a vector database to find the most relevant candidates for any job description.
<img width="1365" height="677" alt="Screenshot 2026-01-28 234556" src="https://github.com/user-attachments/assets/81c07f4b-2072-44ff-83f9-68a62904ff37" />

<img width="1364" height="672" alt="Screenshot 2026-01-28 234730" src="https://github.com/user-attachments/assets/fa9372a4-bf83-435c-a53b-9fd8d5754e70" />

<img width="1364" height="680" alt="Screenshot 2026-01-28 235412" src="https://github.com/user-attachments/assets/63638d47-b97f-4c9d-999f-8ed9ac0f53a4" />

<img width="1364" height="673" alt="Screenshot 2026-01-28 235532" src="https://github.com/user-attachments/assets/8b3cc681-fa7c-4f4c-ba09-9adf348723d9" />

<img width="1317" height="624" alt="Screenshot 2026-01-28 143131" src="https://github.com/user-attachments/assets/32f9d32d-12c5-4275-94e0-a92e546d0280" />


---

## 🚀 Features

- 📂 Upload and manage hundreds of resumes (PDF)
- 🧠 Semantic search using **Sentence-BERT embeddings**
- ⚡ Fast retrieval using **FAISS vector database**
- 🧩 Automatic **document chunking** for better long-resume matching
- 🏷️ **Auto-classification** of resumes into:
  - Civil
  - Mechanical
  - Electrical
  - IT / Software
  - Finance
  - Other
- 🔍 AI-based ranking of candidates against any job description
- 🧠 **Skill extraction** from resumes
- 📌 **Explainable AI**: shows exact resume sections that matched
- 🎯 Sidebar filter by category
- 💾 Persistent index (save/load) for fast startup
- 🖥️ Clean **Streamlit web interface**

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Sentence-Transformers (BERT embeddings)
- FAISS (Vector Database)
- NLP (Text processing, semantic search)
- PyPDF

---

## 🧠 How It Works

1. Upload resumes (PDF files)
2. The system extracts and chunks text from each resume
3. Each chunk is converted into a vector using a Transformer model
4. All vectors are stored in a FAISS index
5. A job description is converted into a vector and searched against the index
6. Top matching resume sections are retrieved and aggregated
7. Candidates are ranked and displayed with:
   - Matching sections
   - Extracted skills
   - Category (IT/Civil/Mechanical/etc.)

---

## ▶️ How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-screener.git
cd ai-resume-screener
pip install -r requirements.txt
streamlit run app.py
```
---
## 🌐 Live Demo

> 🔗 **Deployed App:** https://ai-resume-screener-dk.streamlit.app/

---

## 💼 Real-World Use Case

This system is designed for **recruitment consultancies and HR teams** to:

- Automatically segregate resumes by domain  
- Quickly shortlist relevant candidates  
- Reduce manual resume screening time from hours to minutes  

---

## 📈 Future Improvements

- Export shortlisted candidates to Excel  
- Multi-category filtering  
- LLM-based candidate summary and explanation  
- Authentication and multi-user support  
- Cloud deployment for team usage  

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Disha Karmakar**   
