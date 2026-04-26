"""
semantic_matcher/matcher.py
FINAL FIXED VERSION
"""

from semantic_matcher.embedding import get_embedding
from semantic_matcher.similarity import get_similarity
import PyPDF2


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


def load_file(path):
    if path.endswith(".txt"):
        return read_txt(path)
    elif path.endswith(".pdf"):
        return read_pdf(path)
    else:
        raise ValueError("Unsupported file format")


def semantic_match(resume_input, jd_input):

    # ALWAYS convert to TEXT (fixes ALL your errors)
    resume_text = load_file(resume_input) if isinstance(resume_input, str) else str(resume_input)
    jd_text = load_file(jd_input) if isinstance(jd_input, str) else str(jd_input)

    resume_embedding = get_embedding(resume_text)
    jd_embedding = get_embedding(jd_text)

    return float(get_similarity(resume_embedding, jd_embedding))                  