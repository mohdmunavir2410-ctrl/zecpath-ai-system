"""
resume_parser.py

Converts raw resume text into structured data
for ATS scoring and AI screening.
"""

from section_parser.section_classifier import classify_sections


# --------------------------------
# MASTER SKILL DATABASE
# --------------------------------
SKILLS_DB = [
    "python",
    "machine learning",
    "sql",
    "communication",
    "teamwork",
    "data analysis",
]


# --------------------------------
# Detect Skills (Industry ATS Logic)
# --------------------------------
def detect_skills(text):
    text = text.lower()

    detected = []

    for skill in SKILLS_DB:
        if skill in text:
            detected.append(skill)

    return detected


# --------------------------------
# Build Structured Resume
# --------------------------------
def build_structured_resume(text):

    sections = classify_sections(text)

    structured_resume = {
        "skills": detect_skills(text),  # FULL resume scan
        "education": sections.get("education", ""),
        "experience": sections.get("experience", ""),
        "projects": sections.get("projects", ""),
        "certifications": sections.get("certifications", ""),
    }

    return structured_resume