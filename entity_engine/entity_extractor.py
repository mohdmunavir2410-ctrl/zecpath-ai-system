import re

def extract_entities(text):

    entities = {}

    email = re.findall(r"\S+@\S+", text)
    phone = re.findall(r"\b\d{10}\b", text)

    entities["email"] = email[0] if email else ""
    entities["phone"] = phone[0] if phone else ""

    entities["skills"] = re.findall(
        r"python|sql|machine learning|excel",
        text.lower()
    )

    entities["education"] = text.lower()
    entities["experience"] = text.lower()

    return entities