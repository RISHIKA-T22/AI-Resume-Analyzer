import re
from data.skills_db import SKILLS

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))