"""
Zecpath AI Resume Intelligence System - CLEAN FINAL VERSION
"""

import os
import json
import numpy as np

# -----------------------------
# Parsers
# -----------------------------
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.resume_parser import build_structured_resume
from section_parser.section_classifier import classify_sections

# -----------------------------
# ATS + Screening
# -----------------------------
from ats_engine.scorer import score_candidate
from screening_ai.resume_screening import screen_candidate

# -----------------------------
# Skill Engine
# -----------------------------
from skill_engine.skill_extractor import SkillExtractor
from skill_engine.confidence import calculate_confidence

# -----------------------------
# Education + Experience
# -----------------------------
from parsers.education_parser import extract_education, extract_certifications
from parsers.experience_parser import extract_experience
from utils.academic_profile_builder import build_academic_profile, detect_issuer
from ats_engine.education_relevance_engine import score_education_relevance

# -----------------------------
# Semantic Matching
# -----------------------------
from semantic_matcher.matcher import semantic_match

# -----------------------------
# Entity Extraction
# -----------------------------
from entity_engine.entity_extractor import extract_entities


# =================================================
# CLEAN JSON
# =================================================
def clean_json(obj):
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json(i) for i in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj


# =================================================
# SAVE JSON
# =================================================
def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean_json(data), f, indent=4, ensure_ascii=False)


# =================================================
# RESUME LOADER
# =================================================
def extract_resume(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")


# =================================================
# SKILLS
# =================================================
def extract_skills(text):
    skills_db = ["python", "machine learning", "sql", "communication", "data analysis"]
    text = text.lower()
    return [s for s in skills_db if s in text]


# =================================================
# EDUCATION PIPELINE
# =================================================
def process_education(resume_text, job_keywords):
    education = extract_education(resume_text)
    certifications = extract_certifications(resume_text)

    profile = build_academic_profile(education, certifications)
    edu_score = score_education_relevance(profile, job_keywords)

    return profile, edu_score


# =================================================
# FINAL FORMAT
# =================================================
def format_final_output(
    resume_path,
    jd_name,
    skills,
    education,
    experience,
    entities,
    ats_score,
    semantic_score,
    edu_score,
    final_score,
    decision
):

    return {
        "resume": os.path.basename(resume_path),
        "job": jd_name,

        "skills": skills,

        "education": education,

        "experience": experience,

        "entities": {
            "email": entities.get("email", ""),
            "phone": entities.get("phone", ""),
            "skills": entities.get("skills", [])
        },

        "scores": {
            "ats": float(ats_score),
            "semantic": float(round(semantic_score, 2)),
            "education": float(edu_score),
            "final": float(round(final_score, 2))
        },

        "decision": {
            "status": decision,
            "reason": "Based on ATS + Semantic + Education scoring"
        }
    }


# =================================================
# MAIN
# =================================================
def main():

    print("\n🚀 Zecpath AI Started")

    resume_path = input("Enter resume path: ").strip()
    jd_name = input("Enter JD file name (check folder list): ").strip()

    jd_path = os.path.join("Job_Descriptions", jd_name)

    # ---------------- RESUME ----------------
    print("\n📄 Extracting Resume...")
    resume_text = extract_resume(resume_path)

    entities = extract_entities(resume_text)

    sections = classify_sections(resume_text)
    structured = build_structured_resume(resume_text, sections)

    print("📊 Structured Resume Created")

    # ---------------- SKILLS ----------------
    skills = SkillExtractor().extract_skills(resume_text)

    # ---------------- ATS ----------------
    found_skills = extract_skills(resume_text)

    required_skills = {
        "python": 30,
        "machine learning": 30,
        "sql": 20,
        "communication": 20
    }

    ats_score, _ = score_candidate(found_skills, required_skills)

    # ---------------- SCREENING ----------------
    screen_candidate(structured, required_skills)

    # ---------------- EDUCATION ----------------
    job_keywords = ["python", "machine learning", "data science"]
    education, edu_score = process_education(resume_text, job_keywords)

    # ---------------- EXPERIENCE ----------------
    experience = extract_experience(resume_text)

    # ---------------- SEMANTIC ----------------
    print("\n🧠 Semantic Matching...")
    semantic_score = semantic_match(resume_path, jd_path)
    semantic_score = float(semantic_score) * 100

    # ---------------- FINAL SCORE ----------------
    final_score = (ats_score + semantic_score + edu_score) / 3

    if final_score >= 70:
        decision = "Selected"
    elif final_score >= 50:
        decision = "Moderate"
    else:
        decision = "Rejected"

    # ---------------- OUTPUT ----------------
    output = format_final_output(
        resume_path,
        jd_name,
        skills,
        education,
        experience,
        entities,
        ats_score,
        semantic_score,
        edu_score,
        final_score,
        decision
    )

    print("\n📊 FINAL RESULT GENERATED")

    save_json("output/resume_output.json", output)

    # 🔥 THIS IS YOUR REQUIRED OUTPUT
    print(json.dumps(output, indent=4, ensure_ascii=False))

    print("\n✅ CLEAN OUTPUT SAVED SUCCESSFULLY!")


# =================================================
if __name__ == "__main__":
    main()