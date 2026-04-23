from semantic_matcher.embedding import get_embedding
from semantic_matcher.similarity import get_similarity
import PyPDF2


# ----------------------------
# READ FILE FUNCTIONS
# ----------------------------

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# ====================================================
# ⭐ MAIN SEMANTIC MATCH FUNCTION (NEW)
# ====================================================

def semantic_match(resume_path, jd_path):

    # LOAD RESUME
    if resume_path.endswith(".txt"):
        resume_text = read_txt(resume_path)

    elif resume_path.endswith(".pdf"):
        resume_text = read_pdf(resume_path)

    else:
        raise ValueError("Unsupported resume format")

    # LOAD JD
    job_description = read_txt(jd_path)

    # EMBEDDINGS
    resume_embedding = get_embedding(resume_text)
    jd_embedding = get_embedding(job_description)

    # SIMILARITY
    score = get_similarity(resume_embedding, jd_embedding)

    return score
if __name__ == "__main__":

    resume_path = "data/Resumes/resume4.pdf"
    jd_path = "Job Descriptions/AI in Regulatory Affairs Specialist.txt"

    score = semantic_match(resume_path, jd_path)

    print("\n--- RESULT ---")
    print("Similarity Score:", round(score, 2))