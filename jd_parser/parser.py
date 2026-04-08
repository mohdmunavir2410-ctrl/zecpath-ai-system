import re
import json

def extract_skills(text):
    skills = ["python", "java", "sql", "excel", "machine learning","power bi"]
    found = []

    for skill in skills:
        if skill in text.lower():
            found.append(skill)

    return found


def extract_experience(text):
    match = re.search(r'(\d+)\+?\s*years', text.lower())
    return match.group() if match else None


def extract_role(text):
    text = text.lower()

    if "analyst" in text:
        return "Data Analyst"
    elif "engineer" in text:
        return "Software Engineer"
    elif "ml engineer" in text:
        return "ML Engineer"

    return "Not Found"


def extract_education(text):
    if "bachelor" in text.lower() or "b.tech" in text.lower():
        return "Bachelor's Degree"
    return None


def parse_jd(text):
    return {
        "role": extract_role(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }



if __name__ == "__main__":
    with open("sample_jd.txt", "r") as file:
        jd_text = file.read()

    result = parse_jd(jd_text)

    print("\nParsed Job Description:\n")
    print(result)
    print(json.dumps(result,indent=2))