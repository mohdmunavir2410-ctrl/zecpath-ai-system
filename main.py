import os
import json

from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from ats_engine.scorer import score_candidate
from screening_ai.resume_screening import screen_candidate
from parsers.resume_parser import build_structured_resume
from section_parser.section_classifier import classify_sections

# Day 9
from skill_engine.skill_extractor import SkillExtractor
from skill_engine.confidence import calculate_confidence

# Education + Experience
from parsers.education_parser import extract_education, extract_certifications
from parsers.experience_parser import extract_experience, total_experience


# ------------------------------------------------
# Extract Resume Text
# ------------------------------------------------
def extract_resume(file_path):

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format")


# ------------------------------------------------
# Save Files
# ------------------------------------------------
def save_output(text):

    os.makedirs("output", exist_ok=True)

    path = "output/resume.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


def save_sections(sections):

    os.makedirs("output/results", exist_ok=True)

    with open(
        "output/results/resume_sections.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(sections, f, indent=4)


def save_structured_resume(data):

    os.makedirs("output/results", exist_ok=True)

    path = "output/results/structured_resume.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return path


def save_screening_result(data):

    os.makedirs("reports", exist_ok=True)

    path = "reports/screening_result.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return path


def save_skills(data):

    os.makedirs("output/results", exist_ok=True)

    path = "output/results/skills_intelligence.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return path


def save_log(message):

    os.makedirs("logs", exist_ok=True)

    with open("logs/test_log.txt", "a", encoding="utf-8") as log:
        log.write(message + "\n")


# ------------------------------------------------
# OLD ATS Skill Extractor
# ------------------------------------------------
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
    found = []

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return found


# ------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------
def main():

    file_path = input("Enter resume file path: ")

    try:
        print("Extracting resume...")

        # ✅ Resume Text Extraction
        resume_text = extract_resume(file_path)

        output_file = save_output(resume_text)

        # ------------------------------------------------
        # Section Segmentation
        # ------------------------------------------------
        sections = classify_sections(resume_text)

        if not isinstance(sections, dict):
            raise ValueError("Section classifier must return dictionary")

        save_sections(sections)

        print("📑 Sections detected:", list(sections.keys()))

        # ------------------------------------------------
        # Structured Resume
        # ------------------------------------------------
        structured_data = build_structured_resume(resume_text)
        save_structured_resume(structured_data)

        print("📊 Structured Resume Created")

        # ------------------------------------------------
        # ATS Skill Scoring
        # ------------------------------------------------
        found_skills = extract_skills(resume_text)

        required_skills = {
            "python": 30,
            "machine learning": 30,
            "sql": 20,
            "communication": 20
        }

        score, total = score_candidate(
            found_skills,
            required_skills
        )

        print("\n✅ Extraction Completed!")
        print(f"📄 Saved to: {output_file}")
        print(f"🧠 Found Skills: {found_skills}")
        print(f"⭐ ATS Score: {score}/{total}")

        save_log(f"Extraction successful | ATS Score: {score}/{total}")

        # ------------------------------------------------
        # AI Screening
        # ------------------------------------------------
        screening_result = screen_candidate(
            structured_data,
            required_skills
        )

        report_path = save_screening_result(screening_result)

        print("\n🤖 AI Screening Result")
        print(screening_result)
        print(f"📊 Screening report saved: {report_path}")

        # ------------------------------------------------
        # Skill Intelligence Engine
        # ------------------------------------------------
        extractor = SkillExtractor()

        intelligent_skills = extractor.extract_skills(resume_text)

        if isinstance(intelligent_skills, str):
            intelligent_skills = [intelligent_skills]

        confidence_scores = calculate_confidence(
            sections,
            intelligent_skills
        )

        skills_path = save_skills(confidence_scores)

        print("\n🧠 Intelligent Skill Analysis")
        print(confidence_scores)
        print(f"📁 Skill intelligence saved: {skills_path}")

        # ------------------------------------------------
        # ✅ Education Intelligence (FIXED)
        # ------------------------------------------------
        education = extract_education(resume_text)
        certifications = extract_certifications(resume_text)

        print("\n🎓 Education:")
        print(education)

        print("\n📜 Certifications:")
        print(certifications)

        # ------------------------------------------------
        # Experience Intelligence
        # ------------------------------------------------
        experience_data = extract_experience(resume_text)
        total_exp = total_experience(experience_data)

        print("\n💼 Experience Details:")
        print(experience_data)

        print(f"\n⭐ Total Experience: {total_exp} years")

    except Exception as e:
        save_log(f"Error: {str(e)}")
        print("❌ Error:", e)


# ------------------------------------------------
# RUN
# ------------------------------------------------
if __name__ == "__main__":
    main()