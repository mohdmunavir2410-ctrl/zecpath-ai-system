"""
section_classifier.py

Detects resume sections using heading keywords
"""

import re


SECTION_KEYWORDS = {
    "education": ["education", "academic"],
    "experience": ["experience", "work experience", "employment"],
    "skills": ["skills", "technical skills"],
    "projects": ["projects"],
    "certifications": ["certifications", "certificates", "licenses"],
}


def classify_sections(text):

    lines = text.split("\n")

    sections = {
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "other": []
    }

    current_section = "other"

    for line in lines:

        clean_line = line.strip().lower()

        # ---- Detect Section Heading ----
        found = False
        for section, keywords in SECTION_KEYWORDS.items():
            if any(k in clean_line for k in keywords):
                current_section = section
                found = True
                break

        if found:
            continue

        # ---- Store line ----
        sections[current_section].append(line.strip())

    # convert list → text
    for key in sections:
        sections[key] = "\n".join(sections[key])

    return sections