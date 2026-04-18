import os
from parsers.pdf_parser import extract_text_from_pdf
from parsers.cleaner import clean_text
from parsers.normalizer import normalize_text

text = extract_text_from_pdf("sample_resume.pdf")

cleaned = clean_text(text)

final_text = normalize_text(cleaned)

os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

with open("output/resume.txt", "w", encoding="utf-8") as f:
    f.write(final_text)


with open("logs/test_log.txt", "w", encoding="utf-8") as log:
    log.write("Resume extraction successful")

print("✅ Extraction Completed")