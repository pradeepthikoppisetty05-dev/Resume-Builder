def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def render(data):
    personal       = data.get("personal", {})
    summary        = data.get("summary", "")
    skills         = data.get("skills", [])
    education      = data.get("education", [])
    experience     = data.get("experience", [])
    projects       = data.get("projects", [])
    certifications = data.get("certifications", [])
    languages      = data.get("languages", [])

    month_map = {
        "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
        "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12,
        "January":1,"February":2,"March":3,"April":4,"June":6,"July":7,
        "August":8,"September":9,"October":10,"November":11,"December":12
    }

    education = sorted(
        education,
        key=lambda x: (safe_int(x.get("gradYear",0)), month_map.get(x.get("gradMonth",""),0)),
        reverse=True
    )
    experience = sorted(
        experience,
        key=lambda x: (
            9999 if x.get("current") else safe_int(x.get("endYear",0)),
            12   if x.get("current") else month_map.get(x.get("endMonth",""),0)
        ), reverse=True
    )

    # ── Experience ────────────────────────────────────────────────────────────
    # ATS reads plain text — no flex, no floats, just stacked divs
    experience_html = ""
    for exp in experience:
        end_date = "Present" if exp.get("current") else f"{exp.get('endMonth','')} {exp.get('endYear','')}"
        experience_html += f"""
        <div class="item">
          <div class="item-title-line">
            <span class="item-title">{exp.get("title","")}</span>
          </div>
          <div class="item-meta">{exp.get("employer","")}{" | " + exp.get("location","") if exp.get("location") else ""} | {exp.get("startMonth","")} {exp.get("startYear","")} - {end_date}</div>
          {"<div class='item-desc'>" + exp.get('description','') + "</div>" if exp.get('description','').strip() else ""}
        </div>"""

    # ── Education ─────────────────────────────────────────────────────────────
    education_html = ""
    for edu in education:
        gpa_str = f" | GPA: {edu.get('gpa')}" if edu.get("gpa","").strip() else ""
        education_html += f"""
        <div class="item">
          <div class="item-title">{edu.get("degree","")}{" in " + edu.get("field","") if edu.get("field") else ""}</div>
          <div class="item-meta">{edu.get("school","")}{" | " + edu.get("location","") if edu.get("location") else ""} | {edu.get("gradMonth","")} {edu.get("gradYear","")}{gpa_str}</div>
        </div>"""

    # ── Skills — plain comma list (ATS-friendly, no tags/graphics) ────────────
    skills_html = ""
    if skills:
        filtered = [s for s in skills if s.strip()]
        skills_html = f'<p class="ats-list">{", ".join(filtered)}</p>'

    # ── Projects ──────────────────────────────────────────────────────────────
    projects_html = ""
    for proj in projects:
        meta_parts = []
        if proj.get("role","").strip():  meta_parts.append(f"Role: {proj.get('role')}")
        if proj.get("tools","").strip(): meta_parts.append(f"Tools: {proj.get('tools')}")
        meta_html = f'<div class="item-meta">{" | ".join(meta_parts)}</div>' if meta_parts else ""
        desc_html = f'<div class="item-desc">{proj.get("description","")}</div>' if proj.get("description","").strip() else ""
        url_html  = f'<div class="item-meta">{proj.get("url","")}</div>' if proj.get("url","").strip() else ""
        projects_html += f"""
        <div class="item">
          <div class="item-title">{proj.get("title","")}</div>
          {meta_html}{desc_html}{url_html}
        </div>"""

    # ── Certifications ────────────────────────────────────────────────────────
    certifications_html = ""
    for cert in certifications:
        meta_parts = []
        if cert.get("issuingOrg","").strip():  meta_parts.append(cert.get("issuingOrg"))
        if cert.get("achievedDate","").strip(): meta_parts.append(cert.get("achievedDate"))
        meta_html = f'<div class="item-meta">{" | ".join(meta_parts)}</div>' if meta_parts else ""
        url_html  = f'<div class="item-meta">{cert.get("url","")}</div>' if cert.get("url","").strip() else ""
        certifications_html += f"""
        <div class="item">
          <div class="item-title">{cert.get("name","")}</div>
          {meta_html}{url_html}
        </div>"""

    # ── Languages — plain text (ATS cannot parse progress bars) ──────────────
    languages_html = ""
    if languages:
        pairs = [f'{l.get("name","")} ({l.get("level","Intermediate")})' for l in languages if l.get("name","").strip()]
        if pairs:
            languages_html = f'<p class="ats-list">{", ".join(pairs)}</p>'

    # ── Contact block — plain text, no graphics ───────────────────────────────
    name_line = f"{personal.get('firstName','')} {personal.get('lastName','')}".strip()

    contact_parts = []
    if personal.get("city"):
        loc = personal.get("city","")
        if personal.get("country"): loc += ", " + personal.get("country")
        if personal.get("pincode"): loc += " " + personal.get("pincode")
        contact_parts.append(loc)
    if personal.get("phone"):    contact_parts.append(personal.get("phone"))
    if personal.get("email"):    contact_parts.append(personal.get("email"))
    if personal.get("linkedin"): contact_parts.append(personal.get("linkedin"))
    for w in [w for w in personal.get("websites",[]) if w.strip()]:
        contact_parts.append(w)
    contact_html = " | ".join(contact_parts)

    def section(title, content):
        if not content.strip(): return ""
        return f"""<div class="section">
          <div class="section-header">{title}</div>
          {content}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Resume</title>
<style>


#resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}

/* ATS rule: NO colours, NO images, NO multi-column, NO fancy fonts */
#resume-preview body {{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11pt;
  color: #000;
  background: #fff;
  line-height: 1.45;
}}

#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
  padding: 18mm 20mm;
}}

/* ── Header ── */
#resume-preview .ats-header {{
  text-align: center;
  margin-bottom: 14px;
}}

#resume-preview .ats-name {{
  font-size: 20pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #000;
}}

#resume-preview .ats-profession {{
  font-size: 11pt;
  margin-top: 3px;
  color: #000;
}}

#resume-preview .ats-contact {{
  font-size: 9.5pt;
  margin-top: 6px;
  color: #000;
}}

/* ── Section ── */
#resume-preview .section {{
  margin-bottom: 14px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

/* ATS rule: section headers MUST use well-known labels and plain styling */
#resume-preview .section-header {{
  font-size: 11pt;
  font-weight: 700;
  text-transform: uppercase;
  border-bottom: 1px solid #000;
  padding-bottom: 2px;
  margin-bottom: 8px;
  color: #000;
  letter-spacing: 0.5px;
}}

/* ── Items ── */
#resume-preview .item {{
  margin-bottom: 9px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .item-title {{
  font-weight: 700;
  font-size: 11pt;
  color: #000;
}}

#resume-preview .item-meta {{
  font-size: 10pt;
  color: #000;
  margin-top: 1px;
}}

#resume-preview .item-desc {{
  font-size: 10.5pt;
  color: #000;
  margin-top: 3px;
  line-height: 1.45;
}}

/* ── Skill / Language list ── */
#resume-preview .ats-list {{
  font-size: 10.5pt;
  color: #000;
  line-height: 1.7;
}}

/* ── Summary ── */
#resume-preview .ats-summary {{
  font-size: 10.5pt;
  color: #000;
  line-height: 1.55;
}}

@media print {{
  body, html {{ margin: 0; padding: 0; }}

  #resume-preview .page {{
    min-height: 277mm;
    padding: 0;
    margin: 0;
    width: 190mm;
    box-shadow: none;
  }}

  #resume-preview .page:last-child {{
    page-break-after: avoid;
    break-after: avoid;
  }}

  #resume-preview .section{{
    margin-top: 14px;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }}

  #resume-preview.section-header {{
    page-break-after: avoid;
  }}

  #resume-preview .item {{
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }}

  #resume-preview .page-break {{
    display: block;
    page-break-before: always;
    break-before: always;
    height: 0;
    margin: 0;
    padding: 0;
  }}
}}
</style>
</head>
<body>
<div id="resume-preview">
<div class="page">

  <!-- HEADER — name centred, all text plain for ATS parsing -->
  <div class="ats-header">
    <div class="ats-name">{name_line}</div>
    {"<div class='ats-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="ats-contact">{contact_html}</div>
  </div>

  {"<div class='section'><div class='section-header'>Summary</div><div class='ats-summary'>" + summary + "</div></div>" if summary else ""}

  {section("Skills", skills_html)}

  {section("Work Experience", experience_html)}

  {section("Education", education_html)}

  {section("Projects", projects_html)}

  {section("Certifications", certifications_html)}

  {section("Languages", languages_html)}

</div>
</div>
</body>
</html>"""