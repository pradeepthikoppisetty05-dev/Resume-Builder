import re
import random
from datetime import datetime

STRONG_VERBS = [
    "Developed", "Led", "Managed", "Implemented",
    "Executed", "Designed", "Optimized",
    "Coordinated", "Delivered", "Oversaw",
    "Improved", "Administered", "Facilitated"
]

WEAK_REPLACEMENTS = {
    "worked on": "Contributed to",
    "responsible for": "Managed",
    "helped": "Assisted in",
    "did": "Executed",
    "made": "Developed",
    "created": "Designed",
    "developed developed": "Developed"
}


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s,.()\-/:&]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strengthen_verbs(text):
    for weak, strong in WEAK_REPLACEMENTS.items():
        text = re.sub(weak, strong, text, flags=re.IGNORECASE)
    return text


def remove_duplicate_words(text):
    words = text.split()
    cleaned = []
    for word in words:
        if not cleaned or cleaned[-1].lower() != word.lower():
            cleaned.append(word)
    return " ".join(cleaned)


def preprocess_description(text):
    text = clean_text(text)
    text = strengthen_verbs(text)
    text = remove_duplicate_words(text)
    return text


def detect_leadership_title(title):
    leadership_keywords = [
        "manager",
        "lead",
        "head",
        "director",
        "senior",
        "supervisor",
        "principal",
        "chief" 
    ]

    title_lower = title.lower()
    return any(keyword in title_lower for keyword in leadership_keywords)


def calculate_duration_years(exp):
    start_year = exp.get("startYear")
    end_year = exp.get("endYear")

    if not start_year:
        return 0

    try:
        start_year = int(start_year)

        if exp.get("current") or not end_year:
            end_year = datetime.now().year
        else:
            end_year = int(end_year)

        return max(0, end_year - start_year)

    except (ValueError, TypeError):
        return 0


def classify_experience(years):
    if years <= 1:
        return "entry"
    elif years <= 3:
        return "junior"
    elif years <= 7:
        return "mid"
    else:
        return "senior"


def ensure_strong_start(text):

    if not any(text.lower().startswith(v.lower()) for v in STRONG_VERBS):
        text = random.choice(STRONG_VERBS) + " " + text

    return text.capitalize().rstrip(".") + "."


ENTRY_TEMPLATES = [

    lambda t, c: f"""{c}
Gained practical exposure while supporting daily operational tasks.
Built foundational expertise in the role of {t.lower()}.""",

    lambda t, c: f"""{c}
Contributed to team-based initiatives and acquired hands-on experience.
Strengthened core competencies relevant to the {t.lower()} position.""",

    lambda t, c: f"""{c}
Actively participated in assigned responsibilities to build professional skills.
Developed a strong understanding of organizational workflows as a {t.lower()}.""",

    lambda t, c: f"""{c}
Supported senior professionals in achieving department objectives.
Enhanced technical and analytical skills through real-world application.""",

    lambda t, c: f"""{c}
Demonstrated eagerness to learn while maintaining quality standards.
Contributed meaningfully to projects aligned with the {t.lower()} role."""
]


JUNIOR_TEMPLATES = [

    lambda t, c: f"""{c}
Demonstrated growing accountability and efficiency in assigned tasks.
Collaborated within the {t.lower()} role to support operational success.""",

    lambda t, c: f"""{c}
Played an active role in improving workflow processes and productivity.
Contributed to achieving key performance objectives.""",

    lambda t, c: f"""{c}
Enhanced team performance through consistent delivery of quality results.
Maintained strong professional standards in the {t.lower()} capacity.""",

    lambda t, c: f"""{c}
Improved operational effectiveness through attention to detail.
Supported cross-functional efforts aligned with business goals.""",

    lambda t, c: f"""{c}
Strengthened departmental efficiency through proactive problem-solving.
Delivered measurable contributions within the {t.lower()} position."""
]


MID_TEMPLATES = [

    lambda t, c: f"""{c}
Drove process improvements and enhanced overall operational efficiency.
Collaborated cross-functionally as a {t.lower()} to achieve measurable results.""",

    lambda t, c: f"""{c}
Played a key role in executing strategic initiatives and improving performance metrics.
Maintained high standards of quality and productivity.""",

    lambda t, c: f"""{c}
Led important functional responsibilities contributing to business success.
Streamlined workflows to optimize team output.""",

    lambda t, c: f"""{c}
Demonstrated leadership in managing complex assignments.
Improved service delivery and operational performance.""",

    lambda t, c: f"""{c}
Contributed significantly to organizational growth initiatives.
Ensured compliance with best practices and industry standards."""
]


SENIOR_TEMPLATES = [

    lambda t, c: f"""{c}
Provided strategic leadership to drive sustainable business growth.
Oversaw high-impact initiatives within the {t.lower()} capacity.""",

    lambda t, c: f"""{c}
Directed cross-functional teams to achieve long-term organizational objectives.
Improved enterprise-level performance and operational excellence.""",

    lambda t, c: f"""{c}
Led strategic planning and execution across multiple initiatives.
Delivered consistent results aligned with corporate vision.""",

    lambda t, c: f"""{c}
Championed innovation and process transformation initiatives.
Strengthened organizational capabilities and team performance.""",

    lambda t, c: f"""{c}
Oversaw mission-critical operations and strategic development programs.
Ensured sustained growth and competitive advantage."""
]


TEMPLATE_MAP = {
    "entry": ENTRY_TEMPLATES,
    "junior": JUNIOR_TEMPLATES,
    "mid": MID_TEMPLATES,
    "senior": SENIOR_TEMPLATES
}


# MAIN GENERATOR

def generate_professional_description(exp):

    title = exp.get("title", "Professional")
    description = exp.get("originalDescription", "")

    description = preprocess_description(description)

    if not description:
        return "", None

    years = calculate_duration_years(exp)
    level = classify_experience(years)


    if detect_leadership_title(title):
        level = "senior"

    core = ensure_strong_start(description)

    template_group = TEMPLATE_MAP[level]

    last_index = exp.get("lastTemplateIndex")

    if last_index is not None and len(template_group) > 1:
        possible_indexes = [i for i in range(len(template_group)) if i != last_index]
        selected_index = random.choice(possible_indexes)
    else:
        selected_index = random.randint(0, len(template_group) - 1)

    selected_template = template_group[selected_index]

    return selected_template(title, core), selected_index


def is_already_enhanced(text, title):
    
    if not text:
        return False

    enhancement_markers = [
        "Gained practical exposure",
        "Contributed to team-based initiatives",
        "Actively participated in assigned responsibilities",
        "Supported senior professionals in achieving",
        "Demonstrated eagerness to learn",
        "Demonstrated growing accountability",
        "Played an active role in improving workflow",
        "Enhanced team performance through consistent delivery",
        "Improved operational effectiveness",
        "Strengthened departmental efficiency",
        "Drove process improvements",
        "Played a key role in executing strategic",
        "Led important functional responsibilities",
        "Demonstrated leadership in managing complex",
        "Contributed significantly to organizational growth",
        "Provided strategic leadership",
        "Directed cross-functional teams",
        "Led strategic planning and execution",
        "Championed innovation and process transformation",
        "Oversaw mission-critical operations",
    ]

    return any(marker in text for marker in enhancement_markers)


def enhance_experience_batch(experience_list, variation=0):

    enhanced = []

    for exp in experience_list:
        original = exp.get("originalDescription")
    current = exp.get("description", "")
    title = exp.get("title", "")

    if original:
        base_description = original
    else:
        base_description = current

    new_exp = exp.copy()

    if not original:
        new_exp["originalDescription"] = current
    else:
        new_exp["originalDescription"] = original

        description, template_index = generate_professional_description(new_exp)

        if description:
            new_exp["description"] = description
            new_exp["lastTemplateIndex"] = template_index
        else:
            new_exp["description"] = current

        enhanced.append(new_exp)

    return enhanced