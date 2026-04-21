def calculate_confidence(sections, skills):

    confidence = {}

    # Ensure sections is dictionary
    if not isinstance(sections, dict):
        return {}

    # Normalize skills input
    if isinstance(skills, str):
        skills = [skills]

    if isinstance(skills, dict):
        skills = list(skills.keys())

    if not isinstance(skills, list):
        return {}

    # Merge section text
    full_text = " ".join(str(v) for v in sections.values()).lower()

    for skill in skills:

        mentions = full_text.count(skill.lower())

        confidence[skill] = {
            "mentions": mentions,
            "confidence": min(mentions * 20, 100)
        }

    return confidence