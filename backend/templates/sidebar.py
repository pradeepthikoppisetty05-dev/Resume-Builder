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

    # ── Sidebar: Skills as plain list ─────────────────────────────────────────
    skills_html = ""
    if skills:
        skills_html = "<ul class='sd-skill-list'>"
        for s in skills:
            if s.strip():
                skills_html += f"<li>{s}</li>"
        skills_html += "</ul>"

    # ── Sidebar: Languages with thin bars ─────────────────────────────────────
    level_widths = {"Beginner":20,"Elementary":35,"Intermediate":55,
                    "Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    languages_html = ""
    if languages:
        languages_html = "<div class='sd-lang-list'>"
        for lang in languages:
            if not lang.get("name","").strip(): continue
            level = lang.get("level","Intermediate")
            pct   = level_widths.get(level, 55)
            languages_html += f"""
            <div class="sd-lang">
              <div class="sd-lang-row">
                <span class="sd-lang-name">{lang.get("name","")}</span>
                <span class="sd-lang-level">{level}</span>
              </div>
              <div class="sd-track"><div class="sd-fill" style="width:{pct}%"></div></div>
            </div>"""
        languages_html += "</div>"

    # ── Sidebar: Certifications ────────────────────────────────────────────────
    certifications_html = ""
    for cert in certifications:
        url_html = f'<a class="sd-cred" href="{cert.get("url")}" target="_blank">↗</a>' if cert.get("url","").strip() else ""
        certifications_html += f"""
        <div class="sd-cert">
          <div class="sd-cert-name">{cert.get("name","")} {url_html}</div>
          {"<div class='sd-cert-org'>" + cert.get("issuingOrg","") + "</div>" if cert.get("issuingOrg","").strip() else ""}
          {"<div class='sd-cert-date'>" + cert.get("achievedDate","") + "</div>" if cert.get("achievedDate","").strip() else ""}
        </div>"""

    # ── Main: Experience ───────────────────────────────────────────────────────
    experience_html = ""
    for exp in experience:
        end_date = "Present" if exp.get("current") else f"{exp.get('endMonth','')} {exp.get('endYear','')}"
        desc_html = f'<div class="sd-desc">{exp.get("description","")}</div>' if exp.get("description","").strip() else ""
        experience_html += f"""
        <div class="sd-item">
          <div class="sd-item-head">
            <div class="sd-item-left">
              <div class="sd-item-title">{exp.get("title","")}</div>
              <div class="sd-item-org">{exp.get("employer","")}{" &middot; " + exp.get("location","") if exp.get("location") else ""}</div>
            </div>
            <div class="sd-item-date">{exp.get("startMonth","")} {exp.get("startYear","")} &ndash; {end_date}</div>
          </div>
          {desc_html}
        </div>"""

    # ── Main: Education ────────────────────────────────────────────────────────
    education_html = ""
    for edu in education:
        gpa_str = f" &middot; GPA {edu.get('gpa')}" if edu.get("gpa","").strip() else ""
        education_html += f"""
        <div class="sd-item">
          <div class="sd-item-head">
            <div class="sd-item-left">
              <div class="sd-item-title">{edu.get("degree","")}{" &ndash; " + edu.get("field","") if edu.get("field") else ""}</div>
              <div class="sd-item-org">{edu.get("school","")}{", " + edu.get("location","") if edu.get("location") else ""}{gpa_str}</div>
            </div>
            <div class="sd-item-date">{edu.get("gradMonth","")} {edu.get("gradYear","")}</div>
          </div>
        </div>"""

    # ── Main: Projects ─────────────────────────────────────────────────────────
    projects_html = ""
    for proj in projects:
        meta_parts = []
        if proj.get("role","").strip():  meta_parts.append(f"<strong>Role:</strong> {proj.get('role')}")
        if proj.get("tools","").strip(): meta_parts.append(f"<strong>Tools:</strong> {proj.get('tools')}")
        meta_html = f'<div class="sd-item-org">{" &nbsp;|&nbsp; ".join(meta_parts)}</div>' if meta_parts else ""
        desc_html = f'<div class="sd-desc">{proj.get("description","")}</div>' if proj.get("description","").strip() else ""
        url_html  = f'<div class="sd-url"><a href="{proj.get("url")}" target="_blank">{proj.get("url")}</a></div>' if proj.get("url","").strip() else ""
        projects_html += f"""
        <div class="sd-item">
          <div class="sd-item-title">{proj.get("title","")}</div>
          {meta_html}{desc_html}{url_html}
        </div>"""

    # ── Contact (sidebar) ─────────────────────────────────────────────────────
    contact_lines = []
    if personal.get("city"):
        loc = personal.get("city","")
        if personal.get("country"): loc += ", " + personal.get("country")
        contact_lines.append(loc)
    if personal.get("phone"):    contact_lines.append(personal.get("phone"))
    if personal.get("email"):    contact_lines.append(personal.get("email"))
    if personal.get("linkedin"): contact_lines.append(personal.get("linkedin"))
    for w in [w for w in personal.get("websites",[]) if w.strip()]:
        contact_lines.append(w)

    def sidebar_section(title, content):
        if not content.strip(): return ""
        return f"""<div class="sd-sidebar-section">
          <div class="sd-sidebar-header">{title}</div>
          {content}
        </div>"""

    def main_section(title, content):
        if not content.strip(): return ""
        return f"""<div class="sd-main-section">
          <div class="sd-main-header">{title}</div>
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
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 10pt;
  background: #fff;
  color: #1a1a1a;
  line-height: 1.5;
}}

#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
  height: auto;
  display: flex;
  flex-direction: row;
}}

/* ══════════════ SIDEBAR (dark) ══════════════ */
#resume-preview .sidebar {{
  width: 38%;
  background: #1e2430;
  color: #e8eaf0;
  padding: 28px 20px;
  display: flex;
  flex-direction: column;
  gap: 0;
}}

/* Name block */
#resume-preview .sd-name {{
  font-size: 17pt;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.15;
  word-break: break-word;
}}

#resume-preview .sd-profession {{
  font-size: 9pt;
  color: #8fa3c0;
  margin-top: 4px;
  letter-spacing: 0.5px;
  font-style: italic;
}}

/* Contact list */
#resume-preview .sd-contact {{
  margin-top: 14px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #2e3a4e;
}}

#resume-preview .sd-contact-item {{
  font-size: 8.5pt;
  color: #8fa3c0;
  margin-bottom: 4px;
  word-break: break-all;
}}

/* Sidebar section */
#resume-preview .sd-sidebar-section {{
  margin-bottom: 18px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .sd-sidebar-header {{
  font-size: 7.5pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #4a7ab5;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #2e3a4e;
}}

/* Skill list */
#resume-preview .sd-skill-list {{
  list-style: none;
  padding: 0;
}}

#resume-preview .sd-skill-list li {{
  font-size: 9pt;
  color: #c8d4e8;
  padding: 3px 0;
  border-bottom: 1px solid #2a3345;
  line-height: 1.4;
}}

/* Language bars */
#resume-preview .sd-lang-list {{
  display: flex;
  flex-direction: column;
  gap: 10px;
}}

#resume-preview .sd-lang-row {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
}}

#resume-preview .sd-lang-name  {{ font-size: 9pt; color: #e0e8f5; font-weight: 600; }}
#resume-preview .sd-lang-level {{ font-size: 7.5pt; color: #6a849e; font-style: italic; }}

#resume-preview .sd-track {{
  height: 3px;
  background: #2e3a4e;
  border-radius: 2px;
  overflow: hidden;
}}

#resume-preview .sd-fill {{
  height: 100%;
  background: #4a7ab5;
  border-radius: 2px;
}}

/* Certifications in sidebar */
#resume-preview .sd-cert {{
  margin-bottom: 9px;
  padding-bottom: 9px;
  border-bottom: 1px solid #2a3345;
  page-break-inside: avoid;
}}

#resume-preview .sd-cert:last-child {{ border-bottom: none; }}

#resume-preview .sd-cert-name {{
  font-size: 9pt;
  font-weight: 600;
  color: #d0dcef;
}}

#resume-preview .sd-cert-org  {{ font-size: 8pt; color: #7a94b0; margin-top: 1px; }}
#resume-preview .sd-cert-date {{ font-size: 7.5pt; color: #5a7490; margin-top: 1px; font-style: italic; }}

#resume-preview .sd-cred {{
  font-size: 8.5pt;
  color: #4a7ab5;
  text-decoration: none;
}}

/* ══════════════ MAIN (white) ══════════════ */
#resume-preview .main {{
  width: 62%;
  padding: 28px 22px;
  background: #fff;
}}

/* Summary */
#resume-preview .sd-summary {{
  font-size: 9.5pt;
  color: #333;
  line-height: 1.65;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 2px solid #1e2430;
}}

/* Main section */
#resume-preview .sd-main-section {{
  margin-bottom: 18px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .sd-main-header {{
  font-size: 9pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #1e2430;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 2px solid #1e2430;
}}

/* Items */
#resume-preview .sd-item {{
  margin-bottom: 13px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .sd-item-head {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}}

#resume-preview .sd-item-left {{ flex: 1; }}

#resume-preview .sd-item-title {{
  font-size: 10.5pt;
  font-weight: 700;
  color: #111;
}}

#resume-preview .sd-item-org {{
  font-size: 9pt;
  color: #555;
  margin-top: 2px;
}}

#resume-preview .sd-item-date {{
  font-size: 8.5pt;
  color: #888;
  white-space: nowrap;
  text-align: right;
  padding-top: 2px;
  font-style: italic;
}}

#resume-preview .sd-desc {{
  font-size: 9pt;
  color: #444;
  margin-top: 5px;
  line-height: 1.55;
}}

#resume-preview .sd-url a {{
  font-size: 8.5pt;
  color: #4a7ab5;
  text-decoration: none;
  margin-top: 3px;
  display: inline-block;
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

  <!-- DARK SIDEBAR -->
  <div class="sidebar">

    <!-- Name -->
    <div class="sd-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='sd-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}

    <!-- Contact -->
    <div class="sd-contact">
      {"".join(f"<div class='sd-contact-item'>{c}</div>" for c in contact_lines)}
    </div>

    {sidebar_section("Skills", skills_html)}
    {sidebar_section("Languages", languages_html)}
    {sidebar_section("Certifications &amp; Achievements", certifications_html)}

  </div>

  <!-- WHITE MAIN PANEL -->
  <div class="main">

    {"<div class='sd-summary'>" + summary + "</div>" if summary else ""}

    {main_section("Experience", experience_html)}
    {main_section("Education", education_html)}
    {main_section("Projects", projects_html)}

  </div>
</div>
</div>
</body>
</html>"""