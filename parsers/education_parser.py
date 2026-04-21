"""
education_parser.py
Zecpath AI Education + Certification Intelligence
"""

import re


# -------------------------------------------------
# EDUCATION EXTRACTION (SMART VERSION)
# -------------------------------------------------
def extract_education(resume_text):

    education_list = []

    lines = [line.strip() for line in resume_text.split("\n") if line.strip()]

    degree_keywords = [
        "bsc", "msc", "b.tech", "m.tech",
        "bachelor", "master", "mba"
    ]

    for i, line in enumerate(lines):

        # Detect Degree
        if any(k in line.lower() for k in degree_keywords):

            degree = line
            year = ""
            university = ""

            # 🔎 Look ABOVE for graduation year
            for j in range(max(0, i - 4), i):
                year_match = re.search(r"(20\d{2}\s*-\s*20\d{2})", lines[j])
                if year_match:
                    year = year_match.group(1)
                    break

            # 🔎 Look BELOW for university
            for j in range(i + 1, min(i + 4, len(lines))):
                if "university" in lines[j].lower():
                    university = lines[j]
                    break

            education_list.append({
                "degree": degree,
                "university": university,
                "graduation_year": year
            })

    return education_list


# -------------------------------------------------
# CERTIFICATION EXTRACTION (CLEAN VERSION)
# -------------------------------------------------
def extract_certifications(resume_text):

    certifications = []

    cert_keywords = [
        "aws", "google", "coursera", "udemy",
        "azure", "ibm", "machine learning",
        "data science", "certificate",
        "certification", "training",
        "course", "intern"
    ]

    for line in resume_text.split("\n"):

        clean = line.strip()

        if not clean:
            continue

        # Ignore long paragraph lines
        if len(clean.split()) > 10:
            continue

        # Ignore bullet descriptions
        if clean.startswith("•"):
            continue

        if any(k in clean.lower() for k in cert_keywords):
            certifications.append(clean)

    return list(set(certifications))