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

    # ── Skill tags ────────────────────────────────────────────────────────────
    skills_html = ""
    if skills:
        skills_html = "<div class='skill-tags'>"
        for s in skills:
            if s.strip():
                skills_html += f"<span class='tag'>{s}</span>"
        skills_html += "</div>"

    # ── Experience ────────────────────────────────────────────────────────────
    experience_html = ""
    for exp in experience:
        end_date = "Present" if exp.get("current") else f"{exp.get('endMonth','')} {exp.get('endYear','')}"
        experience_html += f"""
        <div class="item">
          <div class="item-row">
            <span class="item-title">{exp.get("title","")}</span>
            <span class="item-date">{exp.get("startMonth","")} {exp.get("startYear","")} &ndash; {end_date}</span>
          </div>
          <div class="item-sub">{exp.get("employer","")}{" &middot; " + exp.get("location","") if exp.get("location") else ""}</div>
          {"<div class='item-desc'>" + exp.get('description','') + "</div>" if exp.get('description','').strip() else ""}
        </div>"""

    # ── Education ─────────────────────────────────────────────────────────────
    education_html = ""
    for edu in education:
        gpa_str = f" &middot; GPA {edu.get('gpa')}" if edu.get("gpa","").strip() else ""
        education_html += f"""
        <div class="item">
          <div class="item-row">
            <span class="item-title">{edu.get("degree","")}{" &ndash; " + edu.get("field","") if edu.get("field") else ""}</span>
            <span class="item-date">{edu.get("gradMonth","")} {edu.get("gradYear","")}</span>
          </div>
          <div class="item-sub">{edu.get("school","")}{", " + edu.get("location","") if edu.get("location") else ""}{gpa_str}</div>
        </div>"""

    # ── Projects ──────────────────────────────────────────────────────────────
    projects_html = ""
    for proj in projects:
        meta_parts = []
        if proj.get("role","").strip():   meta_parts.append(proj.get("role"))
        if proj.get("tools","").strip():  meta_parts.append(proj.get("tools"))
        meta_html = f'<div class="item-sub">{" &middot; ".join(meta_parts)}</div>' if meta_parts else ""
        desc_html = f'<div class="item-desc">{proj.get("description","")}</div>' if proj.get("description","").strip() else ""
        url_html  = f'<div class="item-link"><a href="{proj.get("url")}" target="_blank">{proj.get("url")}</a></div>' if proj.get("url","").strip() else ""
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
        meta_html = f'<div class="item-sub">{" &middot; ".join(meta_parts)}</div>' if meta_parts else ""
        url_html  = f'<a class="badge-link" href="{cert.get("url")}" target="_blank">View &rarr;</a>' if cert.get("url","").strip() else ""
        certifications_html += f"""
        <div class="item">
          <div class="item-row">
            <span class="item-title">{cert.get("name","")}</span>
            {url_html}
          </div>
          {meta_html}
        </div>"""

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

    # ── Websites ──────────────────────────────────────────────────────────────
    websites = [w for w in personal.get("websites", []) if w.strip()]
    contact_items = []
    if personal.get("city"):
        loc = personal.get("city","")
        if personal.get("country"): loc += ", " + personal.get("country")
        contact_items.append(f"<span>{loc}</span>")
    if personal.get("phone"):    contact_items.append(f"<span>{personal.get('phone')}</span>")
    if personal.get("email"):    contact_items.append(f"<span>{personal.get('email')}</span>")
    if personal.get("linkedin"): contact_items.append(f'<span><a href="{personal.get("linkedin")}" target="_blank">{personal.get("linkedin")}</a></span>')
    for w in websites:           contact_items.append(f'<span><a href="{w}" target="_blank">{w}</a></span>')
    contact_html = " <span class='dot'>&bull;</span> ".join(contact_items)

    def section(title, content):
        if not content.strip(): return ""
        return f"""<div class="section">
          <div class="section-header"><span class="accent-bar"></span>{title}</div>
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
  font-size: 10.5pt;
  color: #1a1a2e;
  background: #fff;
  line-height: 1.5;
}}

/* ── Page ── */
#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
  display: flex;
  flex-direction: column;
}}

/* ── Hero header ── */
#resume-preview .hero {{
  background: linear-gradient(135deg, #16213e 0%, #0f3460 60%, #533483 100%);
  color: #fff;
  padding: 28px 28px 22px 28px;
}}

#resume-preview .hero-name {{
  font-size: 26pt;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  line-height: 1.1;
}}

#resume-preview .hero-profession {{
  font-size: 12pt;
  font-weight: 300;
  color: #e0c9ff;
  margin-top: 4px;
  letter-spacing: 0.5px;
}}

#resume-preview .hero-contact {{
  margin-top: 12px;
  font-size: 9pt;
  color: #ccc;
  display: flex;
  flex-wrap: wrap;
  gap: 4px 0;
  align-items: center;
  line-height: 1.8;
}}

#resume-preview .hero-contact a {{ color: #c9b8ff; text-decoration: none; }}
#resume-preview .hero-contact .dot {{ margin: 0 6px; opacity: 0.5; }}

/* ── Body ── */
#resume-preview .body {{
  display: flex;
  flex: 1;
}}

/* ── Left sidebar ── */
#resume-preview .sidebar {{
  width: 34%;
  background: #f4f0ff;
  padding: 22px 18px;
  flex-shrink: 0;
}}

/* ── Main content ── */
#resume-preview .main {{
  width: 66%;
  padding: 22px 22px 22px 24px;
}}

/* ── Section ── */
#resume-preview .section {{
  margin-bottom: 20px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .section-header {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 10pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #0f3460;
  margin-bottom: 10px;
}}

#resume-preview .accent-bar {{
  display: inline-block;
  width: 4px;
  height: 14px;
  background: linear-gradient(180deg, #533483, #0f3460);
  border-radius: 2px;
  flex-shrink: 0;
}}

/* ── Items ── */
#resume-preview .item {{
  margin-bottom: 12px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .item-row {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 8px;
}}

#resume-preview .item-title {{
  font-weight: 700;
  font-size: 10.5pt;
  color: #1a1a2e;
}}

#resume-preview .item-date {{
  font-size: 8.5pt;
  color: #888;
  white-space: nowrap;
  font-style: italic;
}}

#resume-preview .item-sub {{
  font-size: 9.5pt;
  color: #555;
  margin-top: 2px;
}}

#resume-preview .item-desc {{
  font-size: 9.5pt;
  color: #444;
  margin-top: 4px;
  line-height: 1.5;
}}

#resume-preview .item-link a {{
  font-size: 9pt;
  color: #533483;
  text-decoration: none;
}}

#resume-preview .badge-link {{
  font-size: 8.5pt;
  background: #533483;
  color: #fff;
  padding: 1px 7px;
  border-radius: 10px;
  text-decoration: none;
  white-space: nowrap;
}}

/* ── Skill tags ── */
#resume-preview .skill-tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}}

#resume-preview .tag {{
  background: #fff;
  border: 1.5px solid #c9b8ff;
  color: #0f3460;
  font-size: 8.5pt;
  padding: 3px 9px;
  border-radius: 12px;
  font-weight: 600;
}}

/* ── Summary ── */
#resume-preview .summary-text {{
  font-size: 10pt;
  color: #333;
  line-height: 1.6;
}}

/* ── Languages ── */
#resume-preview .lang-grid {{
  display: flex;
  flex-direction: column;
  gap: 9px;
}}

#resume-preview .lang-row {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
}}

#resume-preview .lang-name  {{ font-size: 9.5pt; font-weight: 700; color: #1a1a2e; }}
#resume-preview .lang-level {{ font-size: 8.5pt; color: #888; font-style: italic; }}

#resume-preview .lang-track {{
  height: 4px;
  background: #ddd;
  border-radius: 2px;
  overflow: hidden;
}}

#resume-preview .lang-fill {{
  height: 100%;
  background: linear-gradient(90deg, #533483, #0f3460);
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

  <!-- HERO HEADER -->
  <div class="hero">
    <div class="hero-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='hero-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="hero-contact">{contact_html}</div>
  </div>

  <div class="body">

    <!-- SIDEBAR -->
    <div class="sidebar">

      {section("Skills", skills_html)}

      {section("Education", education_html)}

      {section("Languages", languages_html)}

      {section("Certifications &amp; Achievements", certifications_html)}

    </div>

    <!-- MAIN -->
    <div class="main">

      {"<div class='section'><div class='section-header'><span class='accent-bar'></span>Profile</div><div class='summary-text'>" + summary + "</div></div>" if summary else ""}

      {section("Experience", experience_html)}

      {section("Projects", projects_html)}

    </div>
  </div>
</div>
</div>
</body>
</html>"""