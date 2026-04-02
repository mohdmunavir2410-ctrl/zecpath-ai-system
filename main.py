from parsers.resume_parser import extract_text_from_pdf
from ats_engine.keyword_matcher import extract_skills
from scoring.scorer import score_candidate

def main():
    text = extract_text_from_pdf("data/resume.pdf")
    
    found_skills = extract_skills(text)

    required_skills = {
        "python": 3,
        "sql": 2,
        "machine learning": 4,
        "excel": 1
    }

    score, total = score_candidate(found_skills, required_skills)

    print("Detected Skills:", found_skills)
    print("Score:", score, "/", total)

if __name__ == "__main__":
    main()