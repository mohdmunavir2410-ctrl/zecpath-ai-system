"""
resume_parser.py

Zecpath AI Resume Intelligence System
FINAL STABLE VERSION
"""

import re
from utils.academic_profile_builder import build_academic_profile


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
        "bsc", "msc", "b.tech", "m.tech",
        "bachelor", "master", "phd"
    ]

    for i, line in enumerate(lines):

        if any(d in line.lower() for d in degree_keywords):

            degree = line.strip()
            university = ""
            year = ""

            # Look next lines
            for j in range(i + 1, min(i + 6, len(lines))):

                next_line = lines[j].lower()

                # Institution detection
                if any(word in next_line for word in
                       ["university", "college", "institute"]):
                    university = lines[j].strip()

                # Year detection
                year_match = re.search(
                    r"(20\d{2}\s*[-–]\s*20\d{2}|20\d{2})",
                    lines[j]
                )

                if year_match:
                    year = year_match.group()

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

    keywords = [
        "intern", "internship", "experience",
        "worked", "developer", "engineer",
        "trainee", "role"
    ]

    for i, line in enumerate(lines):

        if any(k in line.lower() for k in keywords):

            role = line.strip()
            duration = ""

            for j in range(i, min(i + 3, len(lines))):

                date_match = re.search(
                    r"(20\d{2}\s*[-–]\s*(Present|20\d{2})|\d{2}/\d{4}\s*[-–]\s*(Present|\d{2}/\d{4}))",
                    lines[j],
                    re.IGNORECASE
                )

                if date_match:
                    duration = date_match.group()
                    break

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
        "python",
        "course",
        "training",
        "certificate",
        "certification"
    ]

    for line in text.split("\n"):

        clean_line = line.strip()

        if not clean_line:
            continue

        if "intern" in clean_line.lower():
            continue

        if len(clean_line.split()) > 15:
            continue

        if clean_line.startswith("•"):
            continue

        for key in keywords:
            if key in clean_line.lower():

                clean_line = re.sub(
                    r"\(.*intern.*\)",
                    "",
                    clean_line,
                    flags=re.IGNORECASE
                ).strip()

                certifications.append(clean_line)
                break

    return list(set(certifications))


# =====================================================
# SKILLS PARSER
# =====================================================
def extract_skills(text):

    skills = {"technical": [], "soft": []}

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
    return min(len(exp), 5)


# =====================================================
# BUILD STRUCTURED RESUME (FINAL PIPELINE)
# =====================================================
def build_structured_resume(text, sections):

    clean_resume = clean_text(text)

    # ---------------------------
    # Skills
    # ---------------------------
    skills_data = extract_skills(clean_resume)
    skills = skills_data["technical"] + skills_data["soft"]

    # ---------------------------
    # Education
    # ---------------------------
    education = extract_education(
        sections.get("education", clean_resume)
    )

    # ---------------------------
    # Certifications
    # ---------------------------
    certifications = extract_certifications(
        sections.get("certifications", clean_resume)
    )

    # ---------------------------
    # Experience (FIXED VERSION)
    # ---------------------------
    experience_text = (
        sections.get("experience", "") +
        sections.get("projects", "") +
        sections.get("certifications", "")
    )

    experience = extract_experience(experience_text)

    # ---------------------------
    # Academic Profile
    # ---------------------------
    academic_profile = build_academic_profile(
        education,
        certifications
    )

    # ---------------------------
    # Final Structured Resume
    # ---------------------------
    structured_resume = {
        "skills": skills,
        "education": education,
        "experience": experience,
        "academic_profile": academic_profile,
        "projects": sections.get("projects", ""),
        "certifications": academic_profile["certifications"]
    }

    print("📊 Structured Resume Created")

    return structured_resume