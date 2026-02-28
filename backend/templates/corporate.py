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

    experience = sorted(
        experience,
        key=lambda x: (
            9999 if x.get("current") else safe_int(x.get("endYear", 0)),
            12   if x.get("current") else month_map.get(x.get("endMonth",""), 0)
        ), reverse=True
    )
    education = sorted(
        education,
        key=lambda x: (safe_int(x.get("gradYear",0)), month_map.get(x.get("gradMonth",""),0)),
        reverse=True
    )

    # ── Experience ────────────────────────────────────────────────────────────
    experience_html = ""
    for exp in experience:
        end_date = "Present" if exp.get("current") else f"{exp.get('endMonth','')} {exp.get('endYear','')}"
        experience_html += f"""
        <div class="item">
          <div class="item-header-row">
            <div class="item-left">
              <div class="item-title">{exp.get("title","")}</div>
              <div class="item-org">{exp.get("employer","")}{" &bull; " + exp.get("location","") if exp.get("location") else ""}</div>
              {"<div class='item-desc'>" + exp.get('description','') + "</div>" if exp.get('description','').strip() else ""}
            </div>
            <div class="item-date">{exp.get("startMonth","")} {exp.get("startYear","")} &ndash; {end_date}</div>
          </div>
        </div>"""

    # ── Education ─────────────────────────────────────────────────────────────
    education_html = ""
    for edu in education:
        gpa_str = f" &bull; GPA: {edu.get('gpa')}" if edu.get("gpa","").strip() else ""
        education_html += f"""
        <div class="item">
          <div class="item-header-row">
            <div class="item-left">
              <div class="item-title">{edu.get("degree","")}{" in " + edu.get("field","") if edu.get("field") else ""}</div>
              <div class="item-org">{edu.get("school","")}{", " + edu.get("location","") if edu.get("location") else ""}{gpa_str}</div>
            </div>
            <div class="item-date">{edu.get("gradMonth","")} {edu.get("gradYear","")}</div>
          </div>
        </div>"""

    # ── Projects ──────────────────────────────────────────────────────────────
    projects_html = ""
    for proj in projects:
        meta_parts = []
        if proj.get("role","").strip():   meta_parts.append(f"<strong>Role:</strong> {proj.get('role')}")
        if proj.get("tools","").strip():  meta_parts.append(f"<strong>Technologies:</strong> {proj.get('tools')}")
        meta_html = f'<div class="item-org">{" &nbsp;|&nbsp; ".join(meta_parts)}</div>' if meta_parts else ""
        desc_html = f'<div class="item-desc">{proj.get("description","")}</div>' if proj.get("description","").strip() else ""
        url_html  = f'<div class="item-url"><a href="{proj.get("url")}" target="_blank">{proj.get("url")}</a></div>' if proj.get("url","").strip() else ""
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
        meta_html = f'<div class="item-org">{" &bull; ".join(meta_parts)}</div>' if meta_parts else ""
        url_html  = f'<a class="cred-link" href="{cert.get("url")}" target="_blank">View Credential</a>' if cert.get("url","").strip() else ""
        certifications_html += f"""
        <div class="item">
          <div class="item-header-row">
            <div class="item-left">
              <div class="item-title">{cert.get("name","")}</div>
              {meta_html}
            </div>
            {url_html}
          </div>
        </div>"""

    # ── Skills — inline comma separated groups ────────────────────────────────
    skills_html = ""
    if skills:
        filtered = [s for s in skills if s.strip()]
        skills_html = f'<div class="skills-inline">{" &nbsp;&bull;&nbsp; ".join(filtered)}</div>'

    # ── Languages ─────────────────────────────────────────────────────────────
    level_widths = {"Beginner":20,"Elementary":35,"Intermediate":55,
                    "Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    languages_html = ""
    if languages:
        languages_html = "<div class='lang-grid'>"
        for lang in languages:
            if not lang.get("name","").strip(): continue
            level = lang.get("level","Intermediate")
            pct   = level_widths.get(level, 55)
            languages_html += f"""
            <div class="lang-item">
              <div class="lang-row">
                <span class="lang-name">{lang.get("name","")}</span>
                <span class="lang-level">{level}</span>
              </div>
              <div class="lang-track"><div class="lang-fill" style="width:{pct}%"></div></div>
            </div>"""
        languages_html += "</div>"

    # ── Contact line ──────────────────────────────────────────────────────────
    contact_parts = []
    if personal.get("city"):
        loc = personal.get("city","")
        if personal.get("country"): loc += ", " + personal.get("country")
        if personal.get("pincode"): loc += " " + personal.get("pincode")
        contact_parts.append(loc)
    if personal.get("phone"):    contact_parts.append(personal.get("phone"))
    if personal.get("email"):    contact_parts.append(personal.get("email"))
    if personal.get("linkedin"): contact_parts.append(f'<a href="{personal.get("linkedin")}" target="_blank">{personal.get("linkedin")}</a>')
    for w in [w for w in personal.get("websites",[]) if w.strip()]:
        contact_parts.append(f'<a href="{w}" target="_blank">{w}</a>')
    contact_html = " &nbsp;&bull;&nbsp; ".join(contact_parts)

    def section(title, content):
        if not content.strip(): return ""
        return f"""<div class="section">
          <div class="section-title">{title}</div>
          <div class="section-rule"></div>
          {content}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Resume</title>
<style>

#resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}

#resume-preview body {{
  font-family: 'Georgia', 'Times New Roman', serif;
  font-size: 10.5pt;
  color: #111;
  background: #fff;
  line-height: 1.5;
}}

#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
  padding: 0;
}}

/* ── Header band ── */
#resume-preview .header-band {{
  background: #1b2a4a;
  color: #fff;
  padding: 26px 28px 20px 28px;
}}

#resume-preview .header-name {{
  font-size: 24pt;
  font-weight: 700;
  letter-spacing: 1px;
  font-family: 'Georgia', serif;
  text-transform: uppercase;
}}

#resume-preview .header-profession {{
  font-size: 11pt;
  font-weight: 400;
  color: #a8bbd8;
  margin-top: 3px;
  font-style: italic;
}}

#resume-preview .header-contact {{
  margin-top: 10px;
  font-size: 9pt;
  color: #c8d8ee;
  line-height: 1.6;
}}

#resume-preview .header-contact a {{ color: #93b8e8; text-decoration: none; }}

/* ── Body padding ── */
#resume-preview .content {{
  padding: 20px 28px 24px 28px;
}}

/* ── Section ── */
#resume-preview .section {{
  margin-bottom: 18px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .section-title {{
  font-size: 10.5pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: #1b2a4a;
  margin-bottom: 5px;
}}

#resume-preview .section-rule {{
  border-top: 2px solid #1b2a4a;
  margin-bottom: 10px;
}}

/* ── Items ── */
#resume-preview .item {{
  margin-bottom: 11px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .item-header-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}}

#resume-preview .item-left {{ flex: 1; }}

#resume-preview .item-title {{
  font-weight: 700;
  font-size: 10.5pt;
  color: #111;
}}

#resume-preview .item-org {{
  font-size: 9.5pt;
  color: #444;
  margin-top: 2px;
  font-style: italic;
}}

#resume-preview .item-date {{
  font-size: 9pt;
  color: #666;
  white-space: nowrap;
  text-align: right;
  padding-top: 1px;
}}

#resume-preview .item-desc {{
  font-size: 9.5pt;
  color: #333;
  margin-top: 4px;
  line-height: 1.5;
}}

#resume-preview .item-url a, #resume-preview .cred-link {{
  font-size: 9pt;
  color: #1b2a4a;
  text-decoration: underline;
}}

/* ── Summary ── */
#resume-preview .summary-text {{
  font-size: 10pt;
  color: #333;
  line-height: 1.6;
}}

/* ── Skills ── */
#resume-preview .skills-inline {{
  font-size: 10pt;
  color: #222;
  line-height: 1.8;
}}

/* ── Languages ── */
#resume-preview .lang-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  column-gap: 20px;
  row-gap: 9px;
}}

#resume-preview .lang-row {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
}}

#resume-preview .lang-name  {{ font-size: 9.5pt; font-weight: 700; }}
#resume-preview .lang-level {{ font-size: 8.5pt; color: #777; font-style: italic; }}

#resume-preview .lang-track {{
  height: 4px;
  background: #dde3ee;
  border-radius: 2px;
  overflow: hidden;
}}

#resume-preview .lang-fill {{
  height: 100%;
  background: #1b2a4a;
  border-radius: 2px;
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

  <!-- HEADER BAND -->
  <div class="header-band">
    <div class="header-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='header-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="header-contact">{contact_html}</div>
  </div>

  <div class="content">
    {"<div class='section'><div class='section-title'>Executive Summary</div><div class='section-rule'></div><div class='summary-text'>" + summary + "</div></div>" if summary else ""}
    {section("Core Competencies", skills_html)}
    {section("Professional Experience", experience_html)}
    {section("Education", education_html)}
    {section("Projects", projects_html)}
    {section("Certifications &amp; Achievements", certifications_html)}
    {section("Languages", languages_html)}
  </div>

</div>
</div>
</body>
</html>"""