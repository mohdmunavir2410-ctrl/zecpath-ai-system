from parsers.pdf_parser import extract_pdf
from parsers.docx_parser import extract_docx

def extract_text(file_path):

    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    else:
        raise ValueError("Unsupported file type")