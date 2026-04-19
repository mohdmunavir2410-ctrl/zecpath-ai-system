def screen_candidate(resume_data, job_requirements):

    candidate_skills = set(
        skill.lower() for skill in resume_data.get("skills", [])
    )

    required_skills = set(
        skill.lower() for skill in job_requirements.keys()
    )

    matched = candidate_skills.intersection(required_skills)

    score = 0
    total = sum(job_requirements.values())

    for skill in matched:
        score += job_requirements[skill]

    percentage = (score / total) * 100 if total else 0

    decision = "Selected" if percentage >= 60 else "Rejected"

    return {
        "matched_skills": list(matched),
        "score": score,
        "percentage": round(percentage, 2),
        "decision": decision
    }