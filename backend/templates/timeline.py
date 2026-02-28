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

    # ── Timeline entry builder ────────────────────────────────────────────────
    def tl_entry(date_str, title, sub, desc="", extra="", node_class="node-exp"):
        return f"""
        <div class="tl-entry">
          <div class="tl-left">
            <div class="tl-date">{date_str}</div>
          </div>
          <div class="tl-spine-col">
            <div class="tl-node {node_class}"></div>
            <div class="tl-line"></div>
          </div>
          <div class="tl-right">
            <div class="tl-title">{title}</div>
            <div class="tl-sub">{sub}</div>
            {f'<div class="tl-desc">{desc}</div>' if desc.strip() else ""}
            {extra}
          </div>
        </div>"""

    # ── Experience entries ────────────────────────────────────────────────────
    experience_html = ""
    for exp in experience:
        end_date = "Present" if exp.get("current") else f"{exp.get('endMonth','')} {exp.get('endYear','')}"
        date_str = f"{exp.get('startYear','')}&ndash;{end_date.split(' ')[-1] if end_date != 'Present' else 'Present'}"
        sub = f"{exp.get('employer','')}{' &middot; ' + exp.get('location','') if exp.get('location') else ''}"
        experience_html += tl_entry(date_str, exp.get("title",""), sub, exp.get("description",""), node_class="node-exp")

    # ── Education entries ─────────────────────────────────────────────────────
    education_html = ""
    for edu in education:
        gpa_str = f" &middot; GPA {edu.get('gpa')}" if edu.get("gpa","").strip() else ""
        sub = f"{edu.get('school','')}{', ' + edu.get('location','') if edu.get('location') else ''}{gpa_str}"
        title = f"{edu.get('degree','')}{' &ndash; ' + edu.get('field','') if edu.get('field') else ''}"
        education_html += tl_entry(f"{edu.get('gradYear','')}", title, sub, node_class="node-edu")

    # ── Projects ──────────────────────────────────────────────────────────────
    projects_html = ""
    for proj in projects:
        meta_parts = []
        if proj.get("role","").strip():  meta_parts.append(proj.get("role"))
        if proj.get("tools","").strip(): meta_parts.append(proj.get("tools"))
        sub = " &middot; ".join(meta_parts) if meta_parts else ""
        url_html = f'<div class="tl-link"><a href="{proj.get("url")}" target="_blank">{proj.get("url")}</a></div>' if proj.get("url","").strip() else ""
        projects_html += tl_entry("", proj.get("title",""), sub, proj.get("description",""), url_html, node_class="node-proj")

    # ── Certifications ────────────────────────────────────────────────────────
    certifications_html = ""
    for cert in certifications:
        url_html = f'<div class="tl-link"><a href="{cert.get("url")}" target="_blank">View Credential</a></div>' if cert.get("url","").strip() else ""
        certifications_html += tl_entry(
            cert.get("achievedDate",""),
            cert.get("name",""),
            cert.get("issuingOrg",""),
            extra=url_html,
            node_class="node-cert"
        )

    # ── Skills — coloured chips in 3 columns ─────────────────────────────────
    skills_html = ""
    if skills:
        filtered = [s for s in skills if s.strip()]
        skills_html = "<div class='tl-skill-grid'>" + "".join(
            f"<span class='tl-chip'>{s}</span>" for s in filtered
        ) + "</div>"

    # ── Languages ─────────────────────────────────────────────────────────────
    level_widths = {"Beginner":20,"Elementary":35,"Intermediate":55,
                    "Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    languages_html = ""
    if languages:
        languages_html = "<div class='tl-lang-grid'>"
        for lang in languages:
            if not lang.get("name","").strip(): continue
            level = lang.get("level","Intermediate")
            pct   = level_widths.get(level, 55)
            languages_html += f"""
            <div class="tl-lang">
              <div class="tl-lang-row">
                <span class="tl-lang-name">{lang.get("name","")}</span>
                <span class="tl-lang-level">{level}</span>
              </div>
              <div class="tl-track"><div class="tl-fill" style="width:{pct}%"></div></div>
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
    contact_html = " &nbsp;&bull;&nbsp; ".join(contact_parts)

    def section(title, content, node_class="node-exp"):
        if not content.strip(): return ""
        # Section label appears as a special oversized node on the timeline
        return f"""<div class="tl-section">
          <div class="tl-section-head">
            <div class="tl-section-spine">
              <div class="tl-section-node {node_class}"></div>
            </div>
            <div class="tl-section-title">{title}</div>
          </div>
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
  color: #222;
  background: #fff;
  line-height: 1.5;
}}

#resume-preview .page {{
  width: 210mm;
  min-height: 277mm;
}}

/* ── Two-tone header ── */
#resume-preview .tl-header {{
  display: flex;
  min-height: 80px;
}}

#resume-preview .tl-header-left {{
  background: #2d6a4f;
  width: 38%;
  padding: 22px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}}

#resume-preview .tl-header-right {{
  background: #f0f7f4;
  width: 62%;
  padding: 22px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}}

#resume-preview .tl-name {{
  font-size: 18pt;
  font-weight: 700;
  color: #fff;
  line-height: 1.1;
}}

#resume-preview .tl-profession {{
  font-size: 9pt;
  color: #a8d5c2;
  margin-top: 4px;
  font-style: italic;
}}

#resume-preview .tl-contact {{
  font-size: 8.5pt;
  color: #3d5a4c;
  line-height: 1.7;
}}

#resume-preview .tl-contact a {{
  color: #2d6a4f;
  text-decoration: none;
}}

#resume-preview .tl-summary-header {{
  font-size: 8pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #2d6a4f;
  margin-bottom: 4px;
}}

#resume-preview .tl-summary-text {{
  font-size: 8.5pt;
  color: #444;
  line-height: 1.55;
}}

/* ── Body ── */
#resume-preview .tl-body {{
  padding: 16px 20px 20px 20px;
}}

/* ── Section wrapper ── */
#resume-preview .tl-section {{
  margin-bottom: 6px;
  page-break-inside: avoid;
  break-inside: avoid;
}}

#resume-preview .tl-section-head {{
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 2px;
}}

#resume-preview .tl-section-spine {{
  width: 72px;
  flex-shrink: 0;
  display: flex;
  justify-content: flex-end;
  padding-right: 12px;
}}

#resume-preview .tl-section-node {{
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
}}

#resume-preview .tl-section-title {{
  font-size: 10pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: #2d6a4f;
  padding-left: 10px;
  border-left: 2px solid #2d6a4f;
  line-height: 1.3;
}}

/* ── Timeline entry ── */
#resume-preview .tl-entry {{
  display: flex;
  align-items: stretch;
  page-break-inside: avoid;
  break-inside: avoid;
}}

/* Date column */
#resume-preview .tl-left {{
  width: 60px;
  flex-shrink: 0;
  text-align: right;
  padding-right: 8px;
  padding-top: 3px;
}}

#resume-preview .tl-date {{
  font-size: 7.5pt;
  color: #888;
  font-style: italic;
  line-height: 1.3;
}}

/* Spine column */
#resume-preview .tl-spine-col {{
  width: 24px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}}

#resume-preview .tl-node {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
  z-index: 1;
}}

#resume-preview .tl-line {{
  width: 2px;
  flex: 1;
  background: #d4e8de;
  min-height: 14px;
}}

/* Node colours */
#resume-preview .node-exp  {{ background: #2d6a4f; }}
#resume-preview .node-edu  {{ background: #52b788; border: 2px solid #2d6a4f; }}
#resume-preview .node-proj {{ background: #74c69d; }}
#resume-preview .node-cert {{ background: #b7e4c7; border: 1.5px solid #52b788; }}

/* Content column */
#resume-preview .tl-right {{
  flex: 1;
  padding: 2px 0 14px 10px;
}}

#resume-preview .tl-title {{
  font-size: 10pt;
  font-weight: 700;
  color: #111;
}}

#resume-preview .tl-sub {{
  font-size: 8.5pt;
  color: #666;
  margin-top: 1px;
}}

#resume-preview .tl-desc {{
  font-size: 8.5pt;
  color: #444;
  margin-top: 4px;
  line-height: 1.5;
}}

#resume-preview .tl-link a {{
  font-size: 8pt;
  color: #2d6a4f;
  text-decoration: none;
  margin-top: 3px;
  display: inline-block;
}}

/* ── Skills chips ── */
#resume-preview .tl-skill-grid {{
  display: flex;
  flex-wrap: wrap;
  gap: 5px 7px;
  padding: 4px 0 10px 94px;
}}

#resume-preview .tl-chip {{
  font-size: 8pt;
  background: #d8f3dc;
  color: #1b4332;
  padding: 2px 9px;
  border-radius: 10px;
  font-weight: 500;
}}

/* ── Languages ── */
#resume-preview .tl-lang-grid {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 9px 24px;
  padding: 4px 0 10px 94px;
}}

#resume-preview .tl-lang-row {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
}}

#resume-preview .tl-lang-name  {{ font-size: 9pt; font-weight: 600; color: #1b4332; }}
#resume-preview .tl-lang-level {{ font-size: 7.5pt; color: #888; font-style: italic; }}

#resume-preview .tl-track {{
  height: 4px;
  background: #d4e8de;
  border-radius: 2px;
  overflow: hidden;
}}

#resume-preview .tl-fill {{
  height: 100%;
  background: #2d6a4f;
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

  <!-- TWO-TONE HEADER -->
  <div class="tl-header">
    <div class="tl-header-left">
      <div class="tl-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
      {"<div class='tl-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    </div>
    <div class="tl-header-right">
      {"<div class='tl-summary-header'>About</div><div class='tl-summary-text'>" + summary + "</div>" if summary else f"<div class='tl-contact'>{contact_html}</div>"}
    </div>
  </div>
  {"<div style='padding:6px 20px 0 20px'><div class='tl-contact'>" + contact_html + "</div></div>" if summary else ""}

  <!-- TIMELINE BODY -->
  <div class="tl-body">

    {section("Experience", experience_html, "node-exp")}
    {section("Education", education_html, "node-edu")}

    <!-- Skills and Languages (flat, no timeline nodes) -->
    {"<div class='tl-section'><div class='tl-section-head'><div class='tl-section-spine'></div><div class='tl-section-title' style='color:#2d6a4f;border-color:#2d6a4f'>Skills</div></div>" + skills_html + "</div>" if skills_html else ""}
    {"<div class='tl-section'><div class='tl-section-head'><div class='tl-section-spine'></div><div class='tl-section-title' style='color:#2d6a4f;border-color:#2d6a4f'>Languages</div></div>" + languages_html + "</div>" if languages_html else ""}

    {section("Projects", projects_html, "node-proj")}
    {section("Certifications &amp; Achievements", certifications_html, "node-cert")}

  </div>
</div>
</div>
</body>
</html>"""