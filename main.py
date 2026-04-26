import os
import json
import numpy as np

from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx

from parsers.resume_parser import build_structured_resume
from section_parser.section_classifier import classify_sections

from skill_engine.skill_extractor import SkillExtractor
from semantic_matcher.matcher import semantic_match
from ats_engine.scorer import calculate_final_score
from screening_ai.resume_screening import screen_candidate
from entity_engine.entity_extractor import extract_entities


# =====================================================
# FILE READER
# =====================================================
def read_file(path):

    path = os.path.normpath(path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)

    elif path.endswith(".docx"):
        return extract_text_from_docx(path)

    elif path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported format")


# =====================================================
# CLEAN OUTPUT
# =====================================================
def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean(i) for i in obj]
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


# =====================================================
# MAIN PIPELINE
# =====================================================
def main():

    print("\n🚀 Zecpath AI Started")

    resume_path = input("📄 Enter Resume Path: ").strip()
    jd_path = input("📄 Enter Job Description Path: ").strip()

    # ---------------- RESUME ----------------
    print("\n📄 Reading Resume...")
    resume_text = read_file(resume_path)

    sections = classify_sections(resume_text)
    structured_resume = build_structured_resume(resume_text, sections)

    print("📊 Structured Resume Created")

    # ---------------- SKILLS ----------------
    print("\n🧠 Skills Extraction...")
    skills_raw = SkillExtractor().extract_skills(resume_text)

    flat_skills = []
    if isinstance(skills_raw, dict):
        for v in skills_raw.values():
            for item in v:
                if isinstance(item, dict):
                    flat_skills.append(item.get("skill"))
                else:
                    flat_skills.append(item)
    else:
        flat_skills = skills_raw

    flat_skills = [s for s in flat_skills if s]

    print("\n🧠 Skills:", flat_skills)

    # ---------------- ENTITIES ----------------
    entities = extract_entities(resume_text)

    # ---------------- JD ----------------
    print("\n📄 Reading Job Description...")
    jd_text = read_file(jd_path)

    # ---------------- SEMANTIC ----------------
    print("\n🧠 Semantic Matching...")
    semantic_score = semantic_match(resume_path, jd_path)

    # ---------------- ATS SCORE (FIXED CALL) ----------------
    print("\n📊 ATS Scoring...")

    final_score, breakdown = calculate_final_score(
        skills=flat_skills,
        experience=structured_resume.get("experience", []),
        education=structured_resume.get("education", []),
        embedding_score=semantic_score,
        jd_text=jd_text,
        role="software_engineer"
    )

    # ---------------- SCREENING ----------------
    decision = screen_candidate(structured_resume, {
        "required_skills": ["python", "machine learning", "sql"],
        "min_score": 50
    })

    # ---------------- OUTPUT ----------------
    output = {
        "skills": flat_skills,
        "education": structured_resume.get("education", []),
        "experience": structured_resume.get("experience", []),
        "entities": entities,

        "ats_breakdown": breakdown,
        "final_score": final_score,
        "decision": decision
    }

    print("\n⭐ FINAL SCORE:", final_score)
    print("🎯 DECISION:", decision)

    os.makedirs("output", exist_ok=True)

    with open("output/resume_output.json", "w", encoding="utf-8") as f:
        json.dump(clean(output), f, indent=4)

    print("\n📁 Saved: output/resume_output.json")


if __name__ == "__main__":
    main()