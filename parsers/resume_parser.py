"""
resume_parser.py

Zecpath AI Resume Intelligence System
Clean + Stable Version
"""

import re
from section_parser.section_classifier import classify_sections


# =====================================================
# CLEAN TEXT
# =====================================================
def clean_text(text):
    text = re.sub(r"\r", "", text)
    text = re.sub(r"\n+", "\n", text)
    return text


# =====================================================
# EDUCATION PARSER
# =====================================================
def extract_education(text):

    education = []
    lines = text.split("\n")

    degree_keywords = [
        "bsc", "msc", "bachelor", "master",
        "b.tech", "m.tech", "mba"
    ]

    for i, line in enumerate(lines):

        if any(k in line.lower() for k in degree_keywords):

            degree = line.strip()
            university = ""
            year = ""

            # ---------- university ----------
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j].strip():
                    university = lines[j].strip()
                    break

            # ---------- graduation year ----------
            for j in range(i, min(i + 6, len(lines))):
                year_match = re.search(
                    r"(20\d{2}\s*[-–]\s*20\d{2})",
                    lines[j]
                )
                if year_match:
                    year = year_match.group()
                    break

            education.append({
                "degree": degree,
                "institution": university,
                "graduation_year": year
            })

    return education


# =====================================================
# EXPERIENCE PARSER
# =====================================================
def extract_experience(text):

    experience = []
    lines = text.split("\n")

    for i, line in enumerate(lines):

        if "intern" in line.lower() or "experience" in line.lower():

            role = line.strip()
            duration = ""

            if i + 1 < len(lines):

                date_match = re.search(
                    r"(\d{2}/\d{4}\s*[-–]\s*(Present|\d{2}/\d{4}))",
                    lines[i + 1],
                    re.IGNORECASE
                )

                if date_match:
                    duration = date_match.group()

            experience.append({
                "role": role,
                "duration": duration
            })

    return experience


# =====================================================
# CERTIFICATION PARSER
# =====================================================
def extract_certifications(text):

    certifications = []

    keywords = [
        "machine learning",
        "deep learning",
        "data science",
        "python certification",
        "course",
        "training",
        "certificate"
    ]

    for line in text.split("\n"):

        clean_line = line.strip()

        # ignore empty
        if not clean_line:
            continue

        # ignore long paragraph lines
        if len(clean_line.split()) > 12:
            continue

        # ignore bullets
        if clean_line.startswith("•"):
            continue

        for key in keywords:
            if key in clean_line.lower():
                certifications.append(clean_line)
                break

    return list(set(certifications))


# =====================================================
# SKILLS PARSER
# =====================================================
def extract_skills(text):

    skills = {
        "technical": [],
        "soft": []
    }

    tech_skills = [
        "python", "sql", "numpy", "pandas",
        "machine learning", "tensorflow",
        "keras", "power bi", "tableau"
    ]

    soft_skills = [
        "communication",
        "problem solving",
        "time management",
        "teamwork"
    ]

    lower_text = text.lower()

    for skill in tech_skills:
        if skill in lower_text:
            skills["technical"].append(skill)

    for skill in soft_skills:
        if skill in lower_text:
            skills["soft"].append(skill)

    return skills


# =====================================================
# EXPERIENCE CALCULATOR
# =====================================================
def calculate_experience(exp):

    if not exp:
        return 0

    # Internship counted as 1 year (simple logic)
    return 1


# =====================================================
# BUILD STRUCTURED RESUME (CORE ENGINE)
# =====================================================
def build_structured_resume(text):

    text = clean_text(text)

    sections = classify_sections(text)

    skills_data = extract_skills(text)

    # Convert dict → flat list for ATS + Screening
    skills = skills_data["technical"] + skills_data["soft"]

    structured_resume = {
        "skills": skills,
        "education": sections.get("education", ""),
        "experience": sections.get("experience", ""),
        "projects": sections.get("projects", ""),
        "certifications": sections.get("certifications", "")
    }

    return structured_resume