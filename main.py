import os
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from ats_engine.scorer import score_candidate


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

        extracted_text = extract_resume(file_path)

        # Save output
        output_file = save_output(extracted_text)

        # Extract skills
        found_skills = extract_skills(extracted_text)

        # Required skills with weight
        required_skills = {
            "python": 30,
            "machine learning": 30,
            "sql": 20,
            "communication": 20
        }

        # Calculate ATS Score
        score, total = score_candidate(found_skills, required_skills)

        print("\n✅ Extraction Completed!")
        print(f"📄 Saved to: {output_file}")
        print(f"🧠 Found Skills: {found_skills}")
        print(f"⭐ ATS Score: {score}/{total}")

        save_log(f"Extraction successful | ATS Score: {score}/{total}")

    except Exception as e:
        save_log(f"Error: {str(e)}")
        print("❌ Error:", e)


if __name__ == "__main__":
    main()