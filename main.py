import os
import json

from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from ats_engine.scorer import score_candidate
from screening_ai.resume_screening import screen_candidate
from parsers.resume_parser import build_structured_resume
from section_parser.section_classifier import classify_sections


# -----------------------------
# Detect file type & extract text
# -----------------------------
def extract_resume(file_path):

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format")


# -----------------------------
# Save extracted text
# -----------------------------
def save_output(text):

    os.makedirs("output", exist_ok=True)

    output_path = "output/resume.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path


# -----------------------------
# Save Section Output
# -----------------------------
def save_sections(sections):

    os.makedirs("output/results", exist_ok=True)

    with open(
        "output/results/resume_sections.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(sections, f, indent=4)


# -----------------------------
# ✅ NEW — Save Structured Resume
# -----------------------------
def save_structured_resume(data):

    os.makedirs("output/results", exist_ok=True)

    path = "output/results/structured_resume.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return path


# -----------------------------
# ✅ NEW — Save Screening Result
# -----------------------------
def save_screening_result(data):

    os.makedirs("reports", exist_ok=True)

    path = "reports/screening_result.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return path


# -----------------------------
# Save logs
# -----------------------------
def save_log(message):

    os.makedirs("logs", exist_ok=True)

    with open("logs/test_log.txt", "a", encoding="utf-8") as log:
        log.write(message + "\n")


# -----------------------------
# Simple Skill Extractor
# -----------------------------
def extract_skills(text):

    skills_db = [
        "python",
        "machine learning",
        "sql",
        "communication",
        "teamwork",
        "data analysis"
    ]

    text = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# -----------------------------
# MAIN PROGRAM
# -----------------------------
def main():

    file_path = input("Enter resume file path: ")

    try:
        print("Extracting resume...")

        # -----------------------------
        # Resume Extraction
        # -----------------------------
        extracted_text = extract_resume(file_path)

        # Save raw output
        output_file = save_output(extracted_text)

        # -----------------------------
        # DAY 8 — Section Segmentation
        # -----------------------------
        sections = classify_sections(extracted_text)
        save_sections(sections)

        print("📑 Sections detected:", list(sections.keys()))

        # -----------------------------
        # ✅ NEW — Structured Resume
        # -----------------------------
        structured_data = build_structured_resume(extracted_text)

        structured_path = save_structured_resume(structured_data)

        print("📊 Structured Resume Created")

        # -----------------------------
        # Skill Extraction
        # -----------------------------
        found_skills = extract_skills(extracted_text)

        required_skills = {
            "python": 30,
            "machine learning": 30,
            "sql": 20,
            "communication": 20
        }

        # -----------------------------
        # ATS Score Calculation
        # -----------------------------
        score, total = score_candidate(
            found_skills,
            required_skills
        )

        print("\n✅ Extraction Completed!")
        print(f"📄 Saved to: {output_file}")
        print(f"🧠 Found Skills: {found_skills}")
        print(f"⭐ ATS Score: {score}/{total}")

        save_log(f"Extraction successful | ATS Score: {score}/{total}")

        # -----------------------------
        # ✅ NEW — AI Resume Screening
        # -----------------------------
        screening_result = screen_candidate(
            structured_data,
            required_skills
        )

        report_path = save_screening_result(screening_result)

        print("\n🤖 AI Screening Result")
        print(screening_result)
        print(f"📊 Screening report saved: {report_path}")

    except Exception as e:
        save_log(f"Error: {str(e)}")
        print("❌ Error:", e)


if __name__ == "__main__":
    main()