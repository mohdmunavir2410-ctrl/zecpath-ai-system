from ats_engine.scorer import score_candidate


# =============================
# SAMPLE RESUME DATA
# =============================

resume_data = {
    "skills": ["Python", "SQL", "Machine Learning"],
    "years_experience": 2,
    "education": "BSc Mathematics"
}

# =============================
# SAMPLE JOB DESCRIPTION DATA
# =============================

jd_data = {
    "required_skills": {
        "python": 5,
        "sql": 3,
        "machine learning": 4
    },
    "required_years": 2,
    "education": "BSc"
}

# semantic similarity (mock)
semantic_similarity = 0.85


# =============================
# GENERATE SCORE
# =============================

result = score_candidate(
    resume_data,
    jd_data,
    semantic_similarity,
    role="data_scientist"
)

print("\nFINAL ATS RESULT")
print(result)