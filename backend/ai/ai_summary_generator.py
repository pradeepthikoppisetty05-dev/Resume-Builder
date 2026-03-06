import requests
import re

from ai.experience_classifier import calculate_total_experience
from ai.skill_ranker import rank_skills
from ai.impact_detector import extract_impact_statements
from ai.education_analyzer import extract_education_highlights

OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_LENGTH = 700


def generate_summary_ai(resume_data, variation=0):

    personal = resume_data.get("personal", {})
    role = personal.get("profession", "Professional")

    experience_list = resume_data.get("experience", [])
    total_years = calculate_total_experience(experience_list)

    skills = rank_skills(resume_data)
    impacts = extract_impact_statements(resume_data)
    education = extract_education_highlights(resume_data)

    is_fresher = total_years < 1

    prompt = build_prompt(
        role,
        total_years,
        skills,
        impacts,
        education,
        is_fresher,
        variation
    )

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
        },
    )

    text = response.json()["response"].strip()
    text = clean_output(text)

    if len(text) > MAX_LENGTH:
        text = text[:MAX_LENGTH]

    return text.strip()

def build_prompt(role, total_years, skills, impacts, education, is_fresher, variation):

    skills_text = ", ".join(skills[:5]) if skills else ""
    impact_text = impacts[0] if impacts else ""
    education_text = ", ".join(education) if education else ""

    style_variations = [
        "confident and impact-driven tone",
        "concise and achievement-focused tone",
        "strategic and results-oriented tone"
    ]

    style = style_variations[variation % len(style_variations)]

    if is_fresher:

        return f"""
    You are a professional resume summary writer.

    Write a strong professional summary.

    Candidate Role: {role}
    Experience Level: Fresher
    Education Highlights: {education_text}
    Top Skills: {skills_text}

    Rules:
    - Output only the summary
    - No headings
    - No bullet points
    - 3-4 sentences
    - Professional tone
    - Use a {style}

    Summary:
    """

    else:

        return f"""
    You are a professional resume summary writer.

    Write a strong professional summary.

    Candidate Role: {role}
    Total Experience: {total_years} years
    Top Skills: {skills_text}
    Key Impact: {impact_text}

    Rules:
    - Output only the summary
    - No headings
    - No bullet points
    - 3-4 sentences
    - Professional tone
    - Use a {style}
    - Avoid fluff

    Summary:
    """
        
def clean_output(text):

    text = re.sub(r"^\s*Summary:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*(Sure,|Certainly,|Here is.*?:)\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*#+\s*", "", text)

    return text.strip()
