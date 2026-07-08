import re


def extract_experience(text):
    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*years',
        r'(\d+)\+?\s*yrs',
        r'(\d+)\s*year'
    ]

    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            years.append(int(match))

    if years:
        return max(years)

    return 0