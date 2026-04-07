import os
from parsers.pdf_parser import extract_text_from_pdf
from processing.cleaner import clean_text
from processing.normalizer import normalize_text

# -------- Extract --------
text = extract_text_from_pdf("sample_resume.pdf")

# -------- Clean --------
cleaned = clean_text(text)

# -------- Normalize --------
final_text = normalize_text(cleaned)

# -------- Create folders --------
os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# -------- Save Output --------
with open("output/resume.txt", "w", encoding="utf-8") as f:
    f.write(final_text)

# -------- Save Logs --------
with open("logs/test_log.txt", "w", encoding="utf-8") as log:
    log.write("Resume extraction successful")

print("✅ Extraction Completed")