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

    # Month mapping for chronological sorting
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
        # long-form fallback
        "January": 1, "February": 2, "March": 3, "April": 4,
        "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    # ── Sort Education (latest first) ─────────────────────────────────────────
    education = sorted(
        education,
        key=lambda x: (
            safe_int(x.get("gradYear", 0)),
            month_map.get(x.get("gradMonth", ""), 0)
        ),
        reverse=True
    )

    # ── Sort Experience (latest first, current job first) ─────────────────────
    experience = sorted(
        experience,
        key=lambda x: (
            9999 if x.get("current") else safe_int(x.get("endYear", 0)),
            12   if x.get("current") else month_map.get(x.get("endMonth", ""), 0)
        ),
        reverse=True
    )

    # ── Skills HTML ───────────────────────────────────────────────────────────
    skills_html = ""
    if skills:
        skills_html = "<ul class='skills-list'>"
        for skill in skills:
            if skill.strip():
                skills_html += f"<li>{skill}</li>"
        skills_html += "</ul>"

    # ── Education HTML ────────────────────────────────────────────────────────
    education_html = ""
    for edu in education:
        gpa_li = f"GPA: {edu.get('gpa')}" if edu.get("gpa", "").strip() else ""
        education_html += f"""
        <div class="item">
          <div class="item-title">{edu.get("degree", "")}{" in " + edu.get("field", "") if edu.get("field") else ""}</div>
          <ul>
            <li>{edu.get("school", "")}{", " + edu.get("location", "") if edu.get("location") else ""}</li>
            {edu.get("gradMonth", "")} {edu.get("gradYear", "")}
            { "| " + gpa_li if gpa_li else ""}
          </ul>
        </div>
        """

    # ── Experience HTML ───────────────────────────────────────────────────────
    experience_html = ""
    for exp in experience:
        end_date = (
            "Present"
            if exp.get("current")
            else f"{exp.get('endMonth', '')} {exp.get('endYear', '')}"
        )
        experience_html += f"""
        <div class="item">
          <div class="item-title">{exp.get("title", "")}</div>
          <ul>
            <li>{exp.get("employer", "")}{", " + exp.get("location", "") if exp.get("location") else ""}</li>
            <li>{exp.get("startMonth", "")} {exp.get("startYear", "")} &ndash; {end_date}</li>
          </ul>
          <ul>{"<div class='item-desc'>" + exp.get('description','') + "</div>" if exp.get('description','').strip() else ""}
          </ul>
        </div>
        """

    # ── Projects HTML ─────────────────────────────────────────────────────────
    projects_html = ""
    for proj in projects:
        extras = []
        if proj.get("role", "").strip():
            extras.append(f"<li><strong>Role:</strong> {proj.get('role')}</li>")
        if proj.get("tools", "").strip():
            extras.append(f"<li><strong>Tools &amp; Tech:</strong> {proj.get('tools')}</li>")
        if proj.get("description", "").strip():
            extras.append(f"<li>{proj.get('description')}</li>")
        if proj.get("url", "").strip():
            extras.append(f'<li><a href="{proj.get("url")}" target="_blank" class="item-link">{proj.get("url")}</a></li>')

        projects_html += f"""
        <div class="item">
          <div class="item-title">{proj.get("title", "")}</div>
          {"<ul>" + "".join(extras) + "</ul>" if extras else ""}
        </div>
        """

    # ── Certifications HTML ───────────────────────────────────────────────────
    certifications_html = ""
    for cert in certifications:
        details = []
        if cert.get("issuingOrg", "").strip():
            details.append(f"<li>{cert.get('issuingOrg')}</li>")
        if cert.get("achievedDate", "").strip():
            details.append(f"<li>{cert.get('achievedDate')}</li>")
        if cert.get("url", "").strip():
            details.append(f'<li><a href="{cert.get("url")}" target="_blank" class="item-link">View Credential</a></li>')

        certifications_html += f"""
        <div class="item">
          <div class="item-title">{cert.get("name", "")}</div>
          {"<ul>" + "".join(details) + "</ul>" if details else ""}
        </div>
        """

    # ── Languages HTML (progress bars) ───────────────────────────────────────
    level_widths = {
        "Beginner":           20,
        "Elementary":         35,
        "Intermediate":       55,
        "Upper Intermediate": 70,
        "Advanced":           85,
        "Native":             100,
        "Native / Bilingual": 100,
    }

    languages_html = ""
    if languages:
        languages_html = "<div class='lang-grid'>"
        for lang in languages:
            if not lang.get("name", "").strip():
                continue
            level = lang.get("level", "Intermediate")
            pct   = level_widths.get(level, 55)
            languages_html += f"""
            <div class="lang-item">
              <div class="lang-name-row">
                <span class="lang-name">{lang.get("name", "")}</span>
                <span class="lang-level">{level}</span>
              </div>
              <div class="lang-bar-bg">
                <div class="lang-bar-fill" style="width:{pct}%"></div>
              </div>
            </div>
            """
        languages_html += "</div>"

    # ── Websites ──────────────────────────────────────────────────────────────
    websites = personal.get("websites", [])
    websites_html = ""
    if websites:
        links = [f'<a href="{w}" target="_blank">{w}</a>' for w in websites if w.strip()]
        if links:
            websites_html = "<br>" + " | ".join(links)

    # ── Section builder helper ────────────────────────────────────────────────
    def section(title, content):
        if not content.strip():
            return ""
        return (
            f"<div class='section'>"
            f"<div class='section-header'>{title}</div>"
            f"<div class='section-divider'></div>"
            f"{content}"
            f"</div>"
        )

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Resume</title>

<style>

#resume-preview body {{
  font-family: Cambria, serif;
  font-size: 11.2pt;
  line-height: 1.5;
  color: #111;
  margin: 0;
  background: #ffffff;
}}

#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
  padding: 20mm;
  box-sizing: border-box;
}}

/* ================= HEADER ================= */

#resume-preview .header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
}}

#resume-preview .name {{
  font-size: 24pt;
  font-weight: bold;
  color: #000;
  text-transform: uppercase;
}}

#resume-preview .profession {{
  font-size: 12pt;
  color: #444;
  margin-top: 3px;
  font-style: italic;
}}

#resume-preview .contact {{
  text-align: right;
  font-size: 10.8pt;
  line-height: 1.6;
  color: #333;
}}

#resume-preview .contact a {{
  color: #333;
  text-decoration: none;
}}

/* ================= SECTIONS ================= */

#resume-preview .section {{
  margin-top: 16px;
}}

#resume-preview .section-header {{
  font-size: 13pt;
  font-weight: bold;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
  text-transform: uppercase;
}}

#resume-preview .section-divider {{
  border-top: 1.5px solid #333;
  margin-bottom: 10px;
}}

/* ================= ITEMS ================= */

#resume-preview .item {{
  margin-bottom: 10px;
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}}

#resume-preview .item-title {{
  font-weight: bold;
  margin-bottom: 3px;
}}

/* ================= BULLETS ================= */

#resume-preview ul {{
  margin: 3px 0 3px 18px;
  padding: 0;
}}

#resume-preview li {{
  margin-bottom: 3px;
}}

#resume-preview .skills-list {{
  list-style-type: square;
  column-count: 2;
  column-gap: 20px;
}}

#resume-preview p {{
  margin: 4px 0;
  text-align: left;
}}

#resume-preview .item-link {{
  color: #1d4ed8;
  text-decoration: none;
  font-size: 10.5pt;
}}

/* ================= LANGUAGES ================= */

#resume-preview .lang-grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 28px;
  row-gap: 10px;
}}

#resume-preview .lang-item {{
  break-inside: avoid;
}}

#resume-preview .lang-name-row {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 3px;
}}

#resume-preview .lang-name {{
  font-weight: bold;
  font-size: 10.8pt;
}}

#resume-preview .lang-level {{
  font-size: 9.5pt;
  color: #666;
  font-style: italic;
}}

#resume-preview .lang-bar-bg {{
  width: 100%;
  height: 5px;
  background: #ddd;
  border-radius: 3px;
  overflow: hidden;
}}

#resume-preview .lang-bar-fill {{
  height: 100%;
  background: #333;
  border-radius: 3px;
}}

@media print {{
  body, html {{ margin: 0; padding: 0; }}

  #resume-preview .page {{
    min-height: 277mm;
    padding: 0;
    margin: 0;
    width: 190mm
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

    <!-- HEADER -->
    <div class="header">
        <div>
            <div class="name">{personal.get("firstName", "")} {personal.get("lastName", "")}</div>
            {"<div class='profession'>" + personal.get("profession", "") + "</div>" if personal.get("profession") else ""}
        </div>

        <div class="contact">
            {personal.get("email", "") + "<br>" if personal.get("email") else ""}
            {personal.get("phone", "") + "<br>" if personal.get("phone") else ""}
            {personal.get("city", "")}{", " + personal.get("country", "") if personal.get("country") else ""}{" " + personal.get("pincode", "") if personal.get("pincode") else ""}
            {"<br><a href='" + personal.get("linkedin", "") + "' target='_blank'>" + personal.get("linkedin", "") + "</a>" if personal.get("linkedin") else ""}
            {websites_html}
        </div>
    </div>

    <!-- PROFESSIONAL SUMMARY -->
    {section("Professional Summary", "<p>" + summary + "</p>" if summary else "")}

    <!-- TECHNICAL SKILLS -->
    {section("Technical Skills", skills_html)}

    <!-- EDUCATION -->
    {section("Education", education_html)}

    <!-- PROFESSIONAL EXPERIENCE -->
    {section("Professional Experience", experience_html)}

    <!-- PROJECTS -->
    {section("Projects", projects_html)}

    <!-- CERTIFICATIONS & ACHIEVEMENTS -->
    {section("Certifications &amp; Achievements", certifications_html)}

    <!-- LANGUAGES -->
    {section("Languages", languages_html)}
</div>
</div>
</body>
</html>
"""