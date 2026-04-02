from utils import logger
from parsers.resume_parser import extract_text_from_pdf
from ats_engine.keyword_matcher import match_keywords

def start_zecpath_system():
    logger.info("--- Zecpath AI Hiring System Started ---")
    
    resume_path = "data/resume.pdf"
    # Skills we are looking for:
    job_requirements = ["Python", "SQL", "Machine Learning", "Communication"]
    
    # 1. Read the PDF
    resume_text = extract_text_from_pdf(resume_path)
    
    if resume_text:
        # 2. Match Keywords
        match_results = match_keywords(resume_text, job_requirements)
        
        print("\n--- ATS Match Results ---")
        for skill, status in match_results.items():
            print(f"{skill}: {status}")
    else:
        logger.warning("No text was recovered.")

    logger.info("--- System Session Ended ---")

if __name__ == "__main__":
    start_zecpath_system()