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

    # ── Education — academic style: degree bold, thesis/GPA as sub-lines ─────
    education_html = ""
    for edu in education:
        gpa_html = f'<div class="cv-detail">GPA: {edu.get("gpa")}</div>' if edu.get("gpa","").strip() else ""
        education_html += f"""
        <div class="cv-entry">
          <div class="cv-date-col">{edu.get("gradMonth","")} {edu.get("gradYear","")}</div>
          <div class="cv-body-col">
            <div class="cv-title">{edu.get("degree","")}{", " + edu.get("field","") if edu.get("field") else ""}</div>
            <div class="cv-org">{edu.get("school","")}{", " + edu.get("location","") if edu.get("location") else ""}</div>
            
            {gpa_html}
          </div>
        </div>"""

    # ── Experience ────────────────────────────────────────────────────────────
    experience_html = ""
    for exp in experience:
        end_date = "Present" if exp.get("current") else f"{exp.get('endMonth','')} {exp.get('endYear','')}"
        date_str = f"{exp.get('startMonth','')} {exp.get('startYear','')} &ndash; {end_date}"
        experience_html += f"""
        <div class="cv-entry">
          <div class="cv-date-col">{date_str}</div>
          <div class="cv-body-col">
            <div class="cv-title">{exp.get("title","")}</div>
            <div class="cv-org">{exp.get("employer","")}{", " + exp.get("location","") if exp.get("location") else ""}</div>
            {"<div class='cv-desc'>" + exp.get('description','') + "</div>" if exp.get('description','').strip() else ""}
          </div>
        </div>"""

    # ── Projects — academic research / thesis project style ───────────────────
    projects_html = ""
    for proj in projects:
        role_html  = f'<div class="cv-detail"><em>Role:</em> {proj.get("role","")}</div>' if proj.get("role","").strip() else ""
        tools_html = f'<div class="cv-detail"><em>Methods &amp; Tools:</em> {proj.get("tools","")}</div>' if proj.get("tools","").strip() else ""
        desc_html  = f'<div class="cv-desc">{proj.get("description","")}</div>' if proj.get("description","").strip() else ""
        url_html   = f'<div class="cv-detail"><a href="{proj.get("url")}" target="_blank">{proj.get("url")}</a></div>' if proj.get("url","").strip() else ""
        projects_html += f"""
        <div class="cv-entry">
          <div class="cv-date-col"></div>
          <div class="cv-body-col">
            <div class="cv-title">{proj.get("title","")}</div>
            {role_html}{tools_html}{desc_html}{url_html}
          </div>
        </div>"""

    # ── Certifications / Honours ───────────────────────────────────────────────
    certifications_html = ""
    for cert in certifications:
        org_html  = f'<div class="cv-org">{cert.get("issuingOrg","")}</div>' if cert.get("issuingOrg","").strip() else ""
        url_html  = f'<div class="cv-detail"><a href="{cert.get("url")}" target="_blank">View Credential</a></div>' if cert.get("url","").strip() else ""
        certifications_html += f"""
        <div class="cv-entry">
          <div class="cv-date-col">{cert.get("achievedDate","")}</div>
          <div class="cv-body-col">
            <div class="cv-title">{cert.get("name","")}</div>
            {org_html}{url_html}
          </div>
        </div>"""

    # ── Skills — category-style comma list ────────────────────────────────────
    skills_html = ""
    if skills:
        filtered = [s for s in skills if s.strip()]
        skills_html = f'<p class="cv-skills-text">{", ".join(filtered)}</p>'

    # ── Languages ─────────────────────────────────────────────────────────────
    languages_html = ""
    if languages:
        rows = []
        for lang in languages:
            if lang.get("name","").strip():
                rows.append(f'<span class="lang-entry"><strong>{lang.get("name","")}</strong> ({lang.get("level","Intermediate")})</span>')
        if rows:
            languages_html = "<div class='cv-lang-list'>" + " &ensp;&bull;&ensp; ".join(rows) + "</div>"

    # ── Contact / header ──────────────────────────────────────────────────────
    contact_parts = []
    if personal.get("city"):
        loc = personal.get("city","")
        if personal.get("country"): loc += ", " + personal.get("country")
        contact_parts.append(loc)
    if personal.get("phone"):    contact_parts.append(personal.get("phone"))
    if personal.get("email"):    contact_parts.append(f'<a href="mailto:{personal.get("email")}">{personal.get("email")}</a>')
    if personal.get("linkedin"): contact_parts.append(f'<a href="{personal.get("linkedin")}" target="_blank">{personal.get("linkedin")}</a>')
    for w in [w for w in personal.get("websites",[]) if w.strip()]:
        contact_parts.append(f'<a href="{w}" target="_blank">{w}</a>')
    contact_html = " &nbsp;&bull;&nbsp; ".join(contact_parts)

    def section(title, content):
        if not content.strip(): return ""
        return f"""<div class="cv-section">
          <div class="cv-section-header">{title}</div>
          {content}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Curriculum Vitae</title>
<style>

#resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}

#resume-preview body {{
  font-family: 'Times New Roman', Times, serif;
  font-size: 11pt;
  color: #111;
  background: #fff;
  line-height: 1.55;
}}

#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
  padding: 18mm 20mm ;
}}

/* ── CV Header ── */
#resume-preview .cv-header {{
  text-align: center;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 2px solid #111;
}}

#resume-preview .cv-name {{
  font-size: 22pt;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  color: #000;
}}

#resume-preview .cv-profession {{
  font-size: 11pt;
  font-style: italic;
  color: #444;
  margin-top: 3px;
}}

#resume-preview .cv-contact {{
  font-size: 9.5pt;
  color: #444;
  margin-top: 8px;
  line-height: 1.6;
}}

#resume-preview .cv-contact a {{
  color: #333;
  text-decoration: none;
}}

/* ── Section ── */
#resume-preview .cv-section {{
  margin-bottom: 18px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .cv-section-header {{
  font-size: 11pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #000;
  border-bottom: 1px solid #000;
  padding-bottom: 3px;
  margin-bottom: 10px;
}}

/* ── CV entry: date-column + body-column ── */
#resume-preview .cv-entry {{
  display: flex;
  gap: 16px;
  margin-bottom: 10px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .cv-date-col {{
  width: 110px;
  flex-shrink: 0;
  font-size: 9.5pt;
  color: #555;
  font-style: italic;
  padding-top: 1px;
  text-align: right;
}}

#resume-preview .cv-body-col {{
  flex: 1;
}}

#resume-preview .cv-title {{
  font-weight: 700;
  font-size: 11pt;
  color: #000;
}}

#resume-preview .cv-org {{
  font-size: 10pt;
  color: #333;
  margin-top: 1px;
}}

#resume-preview .cv-detail {{
  font-size: 9.5pt;
  color: #555;
  margin-top: 2px;
}}

#resume-preview .cv-detail a {{
  color: #333;
  text-decoration: underline;
}}

#resume-preview .cv-desc {{
  font-size: 10pt;
  color: #333;
  margin-top: 4px;
  line-height: 1.5;
}}

/* ── Skills ── */
#resume-preview .cv-skills-text {{
  font-size: 10.5pt;
  color: #222;
  line-height: 1.7;
}}

/* ── Languages ── */
#resume-preview .cv-lang-list {{
  font-size: 10.5pt;
  color: #222;
  line-height: 1.8;
}}

/* ── Research / summary ── */
#resume-preview .cv-summary {{
  font-size: 10.5pt;
  color: #222;
  line-height: 1.65;
  text-align: justify;
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

  <!-- CV HEADER -->
  <div class="cv-header">
    <div class="cv-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='cv-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="cv-contact">{contact_html}</div>
  </div>

  {"<div class='cv-section'><div class='cv-section-header'>Research &amp; Teaching Interests</div><div class='cv-summary'>" + summary + "</div></div>" if summary else ""}

  {section("Education", education_html)}

  {section("Academic &amp; Professional Experience", experience_html)}

  {section("Research &amp; Projects", projects_html)}

  {section("Skills &amp; Technical Competencies", skills_html)}

  {section("Honours, Awards &amp; Certifications", certifications_html)}

  {section("Languages", languages_html)}
</div>
</div>
</body>
</html>"""