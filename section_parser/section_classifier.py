SECTION_KEYWORDS = {
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "expertise"
    ],
    "experience": [
        "experience",
        "work experience",
        "employment",
        "professional experience"
    ],
    "education": [
        "education",
        "academic background",
        "qualification"
    ],
    "projects": [
        "projects",
        "personal projects"
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses"
    ]
}

def classify_sections(text):

    sections = {}
    current_section = "other"

    lines = text.split("\n")

    for line in lines:
        clean_line = line.lower().strip()

        for section, keywords in SECTION_KEYWORDS.items():
            if any(keyword in clean_line for keyword in keywords):
                current_section = section
                sections[current_section] = ""
                break

        sections.setdefault(current_section, "")
        sections[current_section] += line + "\n"

    return sections