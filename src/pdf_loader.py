# PDF Loader Module
import os
from pypdf import PdfReader

def load_resumes_from_folder(folder_path: str):
    texts = []
    filenames = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            path = os.path.join(folder_path, file)
            reader = PdfReader(path)

            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            if full_text.strip():
                texts.append(full_text)
                filenames.append(file)

    return texts, filenames
