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

# -------- SKILL EXTRACTION  -------- #

skills_list = ["python", "sql", "communication", "java"]

def extract_skills(text):
    text = text.lower()
    found_skills = []
    
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
            
    return found_skills

def confidence(text, skill):
    count = text.count(skill)
    return 0.9 if count > 1 else 0.7

def build_skill_output(text):
    skills = extract_skills(text)
    
    result = []
    for skill in skills:
        result.append({
            "name": skill,
            "confidence": confidence(text, skill)
        })
        
    return result