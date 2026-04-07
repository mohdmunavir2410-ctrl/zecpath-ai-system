def score_candidate(found_skills, required_skills):
    score = 0
    total = 0

    for skill, weight in required_skills.items():
        total += weight
        if skill in found_skills:
            score += weight

    return score, total