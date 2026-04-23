"""
Academic Profile Builder - CLEAN FIXED VERSION
Handles both string and dict certifications safely
"""

def detect_issuer(cert):
    """
    Detect issuer safely for both string and dict inputs
    """

    # If certification is already structured (dict)
    if isinstance(cert, dict):
        return cert.get("issuer", "Unknown")

    # If certification is a string
    if isinstance(cert, str):
        cert_lower = cert.lower()

        if "coursera" in cert_lower:
            return "Coursera"
        elif "udemy" in cert_lower:
            return "Udemy"
        elif "edx" in cert_lower:
            return "edX"
        elif "linkedin" in cert_lower:
            return "LinkedIn Learning"
        else:
            return "Unknown"

    return "Unknown"


def build_academic_profile(education, certifications):
    """
    Builds clean structured academic profile
    Returns DICT (IMPORTANT FIX)
    """

    # ---------------- EDUCATION ----------------
    education_clean = []

    for edu in education:
        if isinstance(edu, dict):
            education_clean.append({
                "degree": edu.get("degree", ""),
                "institution": edu.get("institution", ""),
                "graduation_year": edu.get("graduation_year", "")
            })

    # ---------------- CERTIFICATIONS ----------------
    cert_clean = []

    for cert in certifications:
        if isinstance(cert, dict):
            cert_clean.append({
                "name": cert.get("name", ""),
                "issuer": cert.get("issuer", detect_issuer(cert))
            })

        else:
            cert_clean.append({
                "name": cert,
                "issuer": detect_issuer(cert)
            })

    # ---------------- FINAL OUTPUT (DICT ONLY) ----------------
    return {
        "education": education_clean,
        "certifications": cert_clean
    }