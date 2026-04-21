import re
from datetime import datetime


# -----------------------------------
# Duration Calculator
# -----------------------------------
def calculate_duration(start, end):

    try:
        start_date = datetime.strptime(start, "%b %Y")
    except:
        return 0

    if "present" in end.lower():
        end_date = datetime.now()
    else:
        try:
            end_date = datetime.strptime(end, "%b %Y")
        except:
            return 0

    return (end_date - start_date).days / 365


# -----------------------------------
# Experience Extraction
# -----------------------------------
def extract_experience(text):

    experiences = []

    date_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}\s[-–]\s(Present|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4})"

    lines = text.split("\n")

    for i, line in enumerate(lines):

        match = re.search(date_pattern, line, re.IGNORECASE)

        if match:

            start, end = re.split(r"[-–]", match.group())

            role = lines[i - 1].strip() if i > 0 else "Unknown"
            company = lines[i - 2].strip() if i > 1 else "Unknown"

            duration = calculate_duration(start.strip(), end.strip())

            experiences.append({
                "company": company,
                "role": role,
                "start": start.strip(),
                "end": end.strip(),
                "years": round(duration, 2)
            })

    return experiences


# -----------------------------------
# TOTAL EXPERIENCE FUNCTION
# -----------------------------------
def total_experience(experience_list):

    total = sum(exp["years"] for exp in experience_list)
    return round(total, 2)