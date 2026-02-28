from collections import Counter

def rank_skills(resume_data):
    skills = resume_data.get("skills", [])

    for proj in resume_data.get("projects", []):
        tools = proj.get("tools", "")
        if tools:
            skills.extend([tool.strip() for tool in tools.split(",")])

    cleaned = [skill.strip() for skill in skills if skill.strip()]
    counter = Counter(cleaned)

    ranked = [skill for skill, _ in counter.most_common(5)]
    return ranked