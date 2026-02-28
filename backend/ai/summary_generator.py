from ai.experience_classifier import calculate_total_experience
from ai.skill_ranker import rank_skills
from ai.impact_detector import extract_impact_statements
from ai.education_analyzer import extract_education_highlights
from ai import summary_templates

MAX_LENGTH = 700


def generate_summary(resume_data, variation=0):

    personal = resume_data.get("personal", {})
    role = personal.get("profession", "Professional")

    experience_list = resume_data.get("experience", [])
    total_years = calculate_total_experience(experience_list)

    skills = rank_skills(resume_data)
    impacts = extract_impact_statements(resume_data)
    education = extract_education_highlights(resume_data)

    # FRESHER LOGIC
    if total_years < 1:
        fresher_templates = [
            summary_templates.fresher_template_1,
            summary_templates.fresher_template_2,
            summary_templates.fresher_template_3
        ]

        template = fresher_templates[variation % len(fresher_templates)]
        summary = template(role, education, skills)

    else:
        professional_templates = [
            summary_templates.template_1,
            summary_templates.template_2,
            summary_templates.template_3,
            summary_templates.template_4,
            summary_templates.template_5
        ]

        template = professional_templates[variation % len(professional_templates)]

        impact_text = impacts[0] if impacts else "delivering measurable operational improvements"

        summary = template(role, total_years, skills, impact_text)

    if len(summary) > MAX_LENGTH:
        summary = summary[:MAX_LENGTH]

    return summary.strip()