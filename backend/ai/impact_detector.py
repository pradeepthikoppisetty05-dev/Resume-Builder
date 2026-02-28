import re

IMPACT_PATTERN = r"\b\d+%|\b\d{1,3}(,\d{3})+|\b\d+\+"

def extract_impact_statements(resume_data):
    impacts = []

  
    for exp in resume_data.get("experience", []):
        desc = exp.get("description", "")
        matches = re.findall(IMPACT_PATTERN, desc)
        if matches:
            impacts.append(desc)

   
    for proj in resume_data.get("projects", []):
        desc = proj.get("description", "")
        matches = re.findall(IMPACT_PATTERN, desc)
        if matches:
            impacts.append(desc)

    return impacts[:2]