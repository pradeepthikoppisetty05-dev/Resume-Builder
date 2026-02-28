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
        desc_html = f'<div class="m-desc">{exp.get("description","")}</div>' if exp.get("description","").strip() else ""
        experience_html += f"""
        <div class="m-item">
          <div class="m-date">{exp.get("startMonth","")} {exp.get("startYear","")} &ndash; {end_date}</div>
          <div class="m-content">
            <div class="m-title">{exp.get("title","")}</div>
            <div class="m-sub">{exp.get("employer","")}{" &middot; " + exp.get("location","") if exp.get("location") else ""}</div>
            {desc_html}
          </div>
        </div>"""

    # ── Education ─────────────────────────────────────────────────────────────
    education_html = ""
    for edu in education:
        gpa_str = f" &middot; {edu.get('gpa')}" if edu.get("gpa","").strip() else ""
        education_html += f"""
        <div class="m-item">
          <div class="m-date">{edu.get("gradMonth","")} {edu.get("gradYear","")}</div>
          <div class="m-content">
            <div class="m-title">{edu.get("degree","")}{" &ndash; " + edu.get("field","") if edu.get("field") else ""}</div>
            <div class="m-sub">{edu.get("school","")}{", " + edu.get("location","") if edu.get("location") else ""}{gpa_str}</div>
          </div>
        </div>"""

    # ── Projects ──────────────────────────────────────────────────────────────
    projects_html = ""
    for proj in projects:
        meta_parts = []
        if proj.get("role","").strip():  meta_parts.append(proj.get("role"))
        if proj.get("tools","").strip(): meta_parts.append(proj.get("tools"))
        meta_html = f'<div class="m-sub">{" &middot; ".join(meta_parts)}</div>' if meta_parts else ""
        desc_html = f'<div class="m-desc">{proj.get("description","")}</div>' if proj.get("description","").strip() else ""
        url_html  = f'<div class="m-link"><a href="{proj.get("url")}" target="_blank">{proj.get("url")}</a></div>' if proj.get("url","").strip() else ""
        projects_html += f"""
        <div class="m-item">
          <div class="m-date"></div>
          <div class="m-content">
            <div class="m-title">{proj.get("title","")}</div>
            {meta_html}{desc_html}{url_html}
          </div>
        </div>"""

    # ── Certifications ────────────────────────────────────────────────────────
    certifications_html = ""
    for cert in certifications:
        meta_parts = []
        if cert.get("issuingOrg","").strip():  meta_parts.append(cert.get("issuingOrg"))
        url_html = f'<a class="m-link-inline" href="{cert.get("url")}" target="_blank">↗</a>' if cert.get("url","").strip() else ""
        certifications_html += f"""
        <div class="m-item">
          <div class="m-date">{cert.get("achievedDate","")}</div>
          <div class="m-content">
            <div class="m-title">{cert.get("name","")} {url_html}</div>
            {"<div class='m-sub'>" + cert.get("issuingOrg","") + "</div>" if cert.get("issuingOrg","").strip() else ""}
          </div>
        </div>"""

    # ── Skills — spaced inline ────────────────────────────────────────────────
    skills_html = ""
    if skills:
        filtered = [s for s in skills if s.strip()]
        skills_html = "<div class='m-skills'>" + "".join(
            f"<span class='m-skill'>{s}</span>" for s in filtered
        ) + "</div>"

    # ── Languages ─────────────────────────────────────────────────────────────
    level_widths = {"Beginner":20,"Elementary":35,"Intermediate":55,
                    "Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    languages_html = ""
    if languages:
        languages_html = "<div class='m-lang-list'>"
        for lang in languages:
            if not lang.get("name","").strip(): continue
            level = lang.get("level","Intermediate")
            pct   = level_widths.get(level, 55)
            languages_html += f"""
            <div class="m-lang">
              <div class="m-lang-row">
                <span class="m-lang-name">{lang.get("name","")}</span>
                <span class="m-lang-level">{level}</span>
              </div>
              <div class="m-track"><div class="m-fill" style="width:{pct}%"></div></div>
            </div>"""
        languages_html += "</div>"

    # ── Contact ───────────────────────────────────────────────────────────────
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
    contact_html = " &ensp; ".join(contact_parts)

    def section(title, content):
        if not content.strip(): return ""
        return f"""<div class="m-section">
          <div class="m-section-label">{title}</div>
          <div class="m-section-body">{content}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Resume</title>
<style>

#resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}

#resume-preview body {{
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 9.5pt;
  color: #1a1a1a;
  background: #fff;
  line-height: 1.6;
}}

#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
  padding: 18mm 20mm 18mm 20mm;
}}

/* ── Header ── */
#resume-preview .m-header {{
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 0.5px solid #aaa;
}}

#resume-preview .m-name {{
  font-size: 21pt;
  font-weight: 300;
  letter-spacing: 6px;
  text-transform: uppercase;
  color: #000;
  line-height: 1.1;
}}

#resume-preview .m-profession {{
  font-size: 9pt;
  font-weight: 400;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #888;
  margin-top: 5px;
}}

#resume-preview .m-contact {{
  font-size: 8.5pt;
  color: #666;
  margin-top: 8px;
  letter-spacing: 0.3px;
}}

#resume-preview .m-contact a {{
  color: #444;
  text-decoration: none;
}}

/* ── Section ── */
#resume-preview .m-section {{
  display: flex;
  gap: 0;
  margin-bottom: 18px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .m-section-label {{
  width: 130px;
  flex-shrink: 0;
  font-size: 7.5pt;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #999;
  padding-top: 2px;
  border-top: 0.5px solid #ccc;
  margin-top: 2px;
  padding-top: 6px;
}}

#resume-preview .m-section-body {{
  flex: 1;
  border-top: 0.5px solid #ccc;
  padding-top: 6px;
}}

/* ── Items — date + content ── */
#resume-preview .m-item {{
  display: flex;
  gap: 14px;
  margin-bottom: 14px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .m-date {{
  width: 100px;
  flex-shrink: 0;
  font-size: 8pt;
  color: #999;
  font-style: normal;
  letter-spacing: 0.2px;
  padding-top: 1px;
}}

#resume-preview .m-content {{ flex: 1; }}

#resume-preview .m-title {{
  font-size: 9.5pt;
  font-weight: 600;
  color: #111;
  letter-spacing: 0.2px;
}}

#resume-preview .m-sub {{
  font-size: 8.5pt;
  color: #777;
  margin-top: 2px;
}}

#resume-preview .m-desc {{
  font-size: 8.5pt;
  color: #444;
  margin-top: 4px;
  line-height: 1.55;
}}

#resume-preview .m-link a, #resume-preview .m-link-inline {{
  font-size: 8pt;
  color: #555;
  text-decoration: none;
  border-bottom: 0.5px solid #bbb;
}}

/* ── Skills ── */
#resume-preview .m-skills {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px 10px;
}}

#resume-preview .m-skill {{
  font-size: 8.5pt;
  color: #333;
  padding: 2px 8px;
  border: 0.5px solid #bbb;
  border-radius: 1px;
  letter-spacing: 0.3px;
}}

/* ── Languages ── */
#resume-preview .m-lang-list {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px 24px;
}}

#resume-preview .m-lang-row {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
}}

#resume-preview .m-lang-name  {{ font-size: 8.5pt; font-weight: 600; color: #222; }}
#resume-preview .m-lang-level {{ font-size: 7.5pt; color: #aaa; letter-spacing: 0.5px; }}

#resume-preview .m-track {{
  height: 1px;
  background: #ddd;
  position: relative;
}}

#resume-preview .m-fill {{
  position: absolute;
  top: 0; left: 0;
  height: 100%;
  background: #555;
}}

/* ── Summary ── */
#resume-preview .m-summary {{
  font-size: 9pt;
  color: #444;
  line-height: 1.65;
  max-width: 100%;
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

  <!-- HEADER -->
  <div class="m-header">
    <div class="m-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='m-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="m-contact">{contact_html}</div>
  </div>

  {section("Profile", f"<div class='m-summary'>{summary}</div>") if summary else ""}
  {section("Skills", skills_html)}
  {section("Experience", experience_html)}
  {section("Education", education_html)}
  {section("Projects", projects_html)}
  {section("Certifications", certifications_html)}
  {section("Languages", languages_html)}

</div>
</div>
</body>
</html>"""