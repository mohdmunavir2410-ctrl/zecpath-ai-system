import fitz  # PyMuPDF
import os
from utils import logger


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF resume."""

    if not os.path.exists(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        return None

    try:
        logger.info(f"Starting extraction for: {pdf_path}")

        doc = fitz.open(pdf_path)
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        logger.info("Successfully extracted text from PDF.")
        return text

    except Exception as e:
        logger.error(f"Error during PDF extraction: {e}")
        return None


# Optional local test
if __name__ == "__main__":
    sample_pdf = "data/resume.pdf"
    content = extract_text_from_pdf(sample_pdf)

    if content:
        print("--- Extracted Content Preview ---")
        print(content[:500])