from datetime import datetime

def calculate_total_experience(experience_list):
    total_years = 0
    current_year = datetime.now().year

    for exp in experience_list:
        start_year = exp.get("startYear")
        end_year = exp.get("endYear")

        if not start_year:
            continue

        start_year = int(start_year)

        if exp.get("current"):
            end_year = current_year
        elif end_year:
            end_year = int(end_year)
        else:
            continue

        total_years += max(0, end_year - start_year)

    return total_years


def classify_experience_level(total_years):
    if total_years < 2:
        return "Entry-Level"
    elif total_years < 5:
        return "Mid-Level"
    else:
        return "Senior-Level"