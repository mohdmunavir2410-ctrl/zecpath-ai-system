# AI Data Entity Design Document 

## Objective
To convert unstructured resume and JD content into structured, AI-ready JSON formats.

## Defined Entities
1. **Candidate Profile**: Captures core identity and contact data.
2. **Job Profile**: Captures the essence of the role.
3. **Skill Object**: Separates technical and soft skills for better AI matching.
4. **Experience Object**: Standardizes "Experience patterns" and "Designations."

## Design Logic
- **JSON Format**: Chosen for its compatibility with modern AI models and databases. It supports interoperability(Different AI systems).
- **Arrays (Lists)**: Used for skills and responsibilities to allow AI to iterate through data points easily.
- **Standardization**: Converts varying "Education structures" into a fixed set of keys (degree, institution, year). This reduces data noise.
