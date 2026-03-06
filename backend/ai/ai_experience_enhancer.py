import requests
import re
from ai.experience_enhancer import (
    preprocess_description,
    calculate_duration_years,
    classify_experience,
    detect_leadership_title,
    ensure_strong_start,
)

OLLAMA_URL = "http://localhost:11434/api/generate"


def enhance_with_ai(experience_list, index):

    enhanced = []

    for i, exp in enumerate(experience_list):

        new_exp = exp.copy()

        if i == index:

            original = exp.get("originalDescription")
            current = exp.get("description", "")
            title = exp.get("title", "Professional")

            if original:
                base_description = original
            else:
                base_description = current
                new_exp["originalDescription"] = current

            if base_description.strip():

                cleaned = preprocess_description(base_description)

                years = calculate_duration_years(exp)
                level = classify_experience(years)

                if detect_leadership_title(title):
                    level = "senior"

                core = ensure_strong_start(cleaned)

                enhanced_text = call_ai(core, title, level)

                new_exp["description"] = enhanced_text

        enhanced.append(new_exp)

    return enhanced


def call_ai(description, title, level):

    tone_map = {
        "entry": "entry-level professional",
        "junior": "junior professional",
        "mid": "mid-level professional",
        "senior": "senior-level leader",
    }

    role_context = tone_map.get(level, "professional")

    prompt = f"""
    You are a professional resume rewriting engine.

    TASK:
    Rewrite the experience description below.

    STRICT RULES:
    - Maximum length 325
    - Output ONLY the rewritten experience.
    - Do NOT add explanations.
    - Do NOT add introductions.
    - Do NOT say "Here is"or "Rewritten Experience:".
    - Do NOT use bullet points.
    - Do NOT add headings.
    - Maximum 3 sentences.
    - Professional tone.
    - No fluff.
    - No fake metrics.
    

    Role: {title}
    Seniority: {role_context}

    Original Experience:
    {description}

    
    """
    

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
        },
    )

    text = response.json()["response"].strip()

    text = re.sub(r"^\s*Rewritten Experience:\s*", "", text, flags=re.IGNORECASE)

    text = re.sub(r"^\s*(Sure,|Certainly,|Here is,|here's,|I'd be happy to help!.*?:)\s*", "", text, flags=re.IGNORECASE)

    text = re.sub(r"^\s*#+\s*", "", text)

    text = text.strip()

    return text