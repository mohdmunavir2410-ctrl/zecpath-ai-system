from utils import logger

def match_keywords(text, keywords):
    """Checks if specific keywords exist in the extracted text."""
    if not text:
        logger.error("No text provided for matching.")
        return {}

    logger.info("Starting keyword matching process.")
    results = {}
    
    # Clean the text to make it easier to search
    text_lower = text.lower()
    
    for word in keywords:
        # Check if the word is in the resume
        if word.lower() in text_lower:
            results[word] = "Found"
        else:
            results[word] = "Missing"
            
    logger.info(f"Matching complete. Found {list(results.values()).count('Found')} keywords.")
    return results