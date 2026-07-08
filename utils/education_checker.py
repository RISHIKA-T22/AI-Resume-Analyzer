EDUCATION_KEYWORDS = [
    "b.tech",
    "b.e",
    "bachelor",
    "bachelors",
    "b.sc",
    "m.tech",
    "m.e",
    "master",
    "masters",
    "m.sc",
    "phd",
    "doctorate"
]


def extract_education(text):
    text = text.lower()

    found = []

    for edu in EDUCATION_KEYWORDS:
        if edu in text:
            found.append(edu)

    return list(set(found))