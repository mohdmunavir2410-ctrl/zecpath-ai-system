def extract_skills(text):
    skills = [
        "python", "java", "c++", "sql",
        "machine learning", "data analysis",
        "excel", "communication", "teamwork"
    ]

    text = text.lower()
    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return found_skills