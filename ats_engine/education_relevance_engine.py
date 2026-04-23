"""
education_relevance_engine.py
Zecpath AI - Education Relevance Scoring Engine
"""

def score_education_relevance(profile, job_keywords):

    score = 0

    # -------------------------
    # EDUCATION SCORING
    # -------------------------
    for edu in profile.get("education", []):

        degree = edu.get("degree", "").lower()
        institution = edu.get("institution", "").lower()

        for keyword in job_keywords:

            keyword = keyword.lower()

            if keyword in degree:
                score += 3

            if keyword in institution:
                score += 2

    # -------------------------
    # CERTIFICATION SCORING
    # -------------------------
    for cert in profile.get("certifications", []):

        name = cert.get("name", "").lower()

        for keyword in job_keywords:

            if keyword in name:
                score += 4

    return normalize_score(score)


def normalize_score(score):

    if score > 100:
        return 100

    return score