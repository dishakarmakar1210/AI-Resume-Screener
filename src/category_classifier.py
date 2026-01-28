from src.categories import CATEGORIES

def classify_resume(text: str):
    text = text.lower()

    scores = {cat: 0 for cat in CATEGORIES}

    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text:
                scores[category] += 1

    # Find best category
    best_category = max(scores, key=scores.get)

    # If no keywords matched at all
    if scores[best_category] == 0:
        return "Other"

    return best_category
