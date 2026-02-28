def extract_education_highlights(resume_data):
    education_list = resume_data.get("education", [])
    certifications = resume_data.get("certifications", [])

    highlights = []

    if education_list:
        highest_degree = education_list[0]
        degree = highest_degree.get("degree", "")
        field = highest_degree.get("field", "")
        if degree and field:
            highlights.append(f"{degree} in {field}")

    if certifications:
        cert_names = [cert.get("name") for cert in certifications if cert.get("name")]
        highlights.extend(cert_names[:2])

    return highlights