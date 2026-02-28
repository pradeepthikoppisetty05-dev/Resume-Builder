def safe_int(v):
    try: return int(v)
    except: return 0

def render(data):
    personal       = data.get("personal", {})
    summary        = data.get("summary", "")
    skills         = data.get("skills", [])
    education      = data.get("education", [])
    experience     = data.get("experience", [])
    projects       = data.get("projects", [])
    certifications = data.get("certifications", [])
    languages      = data.get("languages", [])

    month_map = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
                 "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    experience = sorted(experience, key=lambda x:(9999 if x.get("current") else safe_int(x.get("endYear",0)),12 if x.get("current") else month_map.get(x.get("endMonth",""),0)),reverse=True)
    education  = sorted(education,  key=lambda x:(safe_int(x.get("gradYear",0)),month_map.get(x.get("gradMonth",""),0)),reverse=True)

    # pastel accent colours cycle for skill tags
    pastel_colors = ["#e8d5f5","#d5e8f5","#d5f5e8","#f5e8d5","#f5d5e8","#e8f5d5"]
    pastel_text   = ["#6a3d8f","#3d6a8f","#3d8f6a","#8f6a3d","#8f3d6a","#6a8f3d"]

    def sec(title, content):
        if not content.strip(): return ""
        return f"<div class='ps-section'><div class='ps-sec-title'>{title}</div>{content}</div>"

    exp_html = ""
    for e in experience:
        end  = "Present" if e.get("current") else f"{e.get('endMonth','')} {e.get('endYear','')}"
        desc = f"<div class='ps-desc'>{e.get('description','')}</div>" if e.get("description","").strip() else ""
        exp_html += f"""<div class='ps-card'>
          <div class='ps-card-top'><div class='ps-card-left'><div class='ps-title'>{e.get('title','')}</div><div class='ps-sub'>{e.get('employer','')}{' &middot; '+e.get('location','') if e.get('location') else ''}</div></div>
          <span class='ps-date-pill'>{e.get('startYear','')} &ndash; {end.split(' ')[-1] if end != 'Present' else 'Present'}</span></div>{desc}</div>"""

    edu_html = ""
    for e in education:
        gpa = f" &middot; GPA {e.get('gpa')}" if e.get("gpa","").strip() else ""
        edu_html += f"""<div class='ps-card'>
          <div class='ps-card-top'><div class='ps-card-left'><div class='ps-title'>{e.get('degree','')}{' &ndash; '+e.get('field','') if e.get('field') else ''}</div>
          <div class='ps-sub'>{e.get('school','')}{', '+e.get('location','') if e.get('location') else ''}{gpa}</div></div>
          <span class='ps-date-pill'>{e.get('gradYear','')}</span></div></div>"""

    proj_html = ""
    for p in projects:
        parts = []
        if p.get("role","").strip():  parts.append(f"<strong>Role:</strong> {p.get('role')}")
        if p.get("tools","").strip(): parts.append(f"<strong>Stack:</strong> {p.get('tools')}")
        sub_h  = f"<div class='ps-sub'>{' &nbsp;&bull;&nbsp; '.join(parts)}</div>" if parts else ""
        desc_h = f"<div class='ps-desc'>{p.get('description','')}</div>" if p.get("description","").strip() else ""
        url_h  = f"<a class='ps-link' href='{p.get('url')}' target='_blank'>{p.get('url')}</a>" if p.get("url","").strip() else ""
        proj_html += f"<div class='ps-card'><div class='ps-title'>{p.get('title','')}</div>{sub_h}{desc_h}{url_h}</div>"

    cert_html = ""
    for c in certifications:
        parts = []
        if c.get("issuingOrg","").strip():  parts.append(c.get("issuingOrg"))
        if c.get("achievedDate","").strip(): parts.append(c.get("achievedDate"))
        sub_h = f"<div class='ps-sub'>{' &middot; '.join(parts)}</div>" if parts else ""
        url_h = f"<a class='ps-link' href='{c.get('url')}' target='_blank'>View Credential &rarr;</a>" if c.get("url","").strip() else ""
        cert_html += f"<div class='ps-card'><div class='ps-title'>{c.get('name','')}</div>{sub_h}{url_h}</div>"

    sk_html = ""
    if skills:
        filtered = [s for s in skills if s.strip()]
        sk_html = "<div class='ps-skill-wrap'>"
        for i, s in enumerate(filtered):
            bg  = pastel_colors[i % len(pastel_colors)]
            col = pastel_text[i % len(pastel_text)]
            sk_html += f"<span class='ps-skill' style='background:{bg};color:{col};border-color:{bg}'>{s}</span>"
        sk_html += "</div>"

    lv = {"Beginner":20,"Elementary":35,"Intermediate":55,"Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    lang_html = ""
    if languages:
        lang_html = "<div class='ps-lang-grid'>"
        for l in languages:
            if not l.get("name","").strip(): continue
            pct = lv.get(l.get("level","Intermediate"),55)
            lang_html += f"<div class='ps-lang'><div class='ps-lang-row'><span class='ps-lang-name'>{l.get('name','')}</span><span class='ps-lang-lv'>{l.get('level','')}</span></div><div class='ps-bar-bg'><div class='ps-bar-fill' style='width:{pct}%'></div></div></div>"
        lang_html += "</div>"

    websites = [w for w in personal.get("websites",[]) if w.strip()]
    c_parts = []
    if personal.get("city"):
        loc = personal.get("city")
        if personal.get("country"): loc += ", " + personal.get("country")
        c_parts.append(loc)
    if personal.get("phone"):    c_parts.append(personal.get("phone"))
    if personal.get("email"):    c_parts.append(f'<a href="mailto:{personal.get("email")}">{personal.get("email")}</a>')
    if personal.get("linkedin"): c_parts.append(f'<a href="{personal.get("linkedin")}" target="_blank">{personal.get("linkedin")}</a>')
    for w in websites:           c_parts.append(f'<a href="{w}" target="_blank">{w}</a>')
    contact_html = " &nbsp;&bull;&nbsp; ".join(c_parts)

    return f"""
<style>

  #resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}
  #resume-preview {{ font-family:'Segoe UI',Arial,sans-serif; font-size:10pt; color:#2d2d3a; background:#fff; line-height:1.5; }}
  #resume-preview .page {{ width:210mm; min-height:277mm; height:auto;background:#fff; }}

  /* Header */
  #resume-preview .ps-header {{ background:linear-gradient(135deg,#ede7f6 0%,#e3f2fd 100%); padding:24px 22px 18px 22px; }}
  #resume-preview .ps-name {{ font-size:22pt; font-weight:700; color:#2d2d3a; line-height:1.1; }}
  #resume-preview .ps-profession {{ font-size:10pt; color:#7c4daa; margin-top:4px; font-weight:600; }}
  #resume-preview .ps-contact {{ font-size:8.5pt; color:#555; margin-top:8px; line-height:1.7; }}
  #resume-preview .ps-contact a {{ color:#7c4daa; text-decoration:none; }}

  /* Body */
  #resume-preview .ps-body {{ padding:14px 22px; }}

  /* Summary */
  #resume-preview .ps-summary {{ font-size:9.5pt; color:#444; line-height:1.65; margin-bottom:14px; padding:10px 14px; background:#f5f0fb; border-radius:8px; border-left:3px solid #b39ddb; }}

  /* Sections */
  #resume-preview .ps-section {{ margin-bottom:16px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .ps-sec-title {{ font-size:8.5pt; font-weight:700; text-transform:uppercase; letter-spacing:2px; color:#7c4daa; margin-bottom:8px; display:flex; align-items:center; gap:8px; }}
  #resume-preview .ps-sec-title::after {{ content:''; flex:1; height:1px; background:#e1d5f5; }}

  /* Cards */
  #resume-preview .ps-card {{ background:#fdfbff; border:1px solid #ede7f6; border-radius:8px; padding:10px 12px; margin-bottom:8px; page-break-inside:avoid; break-inside:avoid; box-shadow:0 1px 3px rgba(124,77,170,0.07); }}
  #resume-preview .ps-card-top {{ display:flex; justify-content:space-between; align-items:flex-start; gap:8px; }}
  #resume-preview .ps-card-left {{ flex:1; }}
  #resume-preview .ps-title {{ font-weight:700; font-size:10pt; color:#1a1a2e; }}
  #resume-preview .ps-sub {{ font-size:9pt; color:#777; margin-top:2px; }}
  #resume-preview .ps-desc {{ font-size:9pt; color:#444; margin-top:5px; line-height:1.55; }}
  #resume-preview .ps-date-pill {{ font-size:8pt; background:#ede7f6; color:#7c4daa; padding:3px 9px; border-radius:12px; white-space:nowrap; font-weight:600; flex-shrink:0; }}
  #resume-preview .ps-link {{ font-size:8.5pt; color:#7c4daa; text-decoration:none; margin-top:4px; display:inline-block; }}

  /* Skills */
  #resume-preview .ps-skill-wrap {{ display:flex; flex-wrap:wrap; gap:5px 7px; }}
  #resume-preview .ps-skill {{ font-size:8.5pt; padding:3px 11px; border-radius:14px; font-weight:600; border:1px solid; }}

  /* Languages */
  #resume-preview .ps-lang-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px 24px; }}
  #resume-preview .ps-lang-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
  #resume-preview .ps-lang-name {{ font-size:9.5pt; font-weight:700; color:#2d2d3a; }}
  #resume-preview .ps-lang-lv {{ font-size:8pt; color:#aaa; font-style:italic; }}
  #resume-preview .ps-bar-bg {{ height:5px; background:#ede7f6; border-radius:3px; overflow:hidden; }}
  #resume-preview .ps-bar-fill {{ height:100%; background:#b39ddb; border-radius:3px; }}

  @media print {{
    #resume-preview .ps-header {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .ps-section {{ page-break-inside:avoid; break-inside:avoid; }}
    #resume-preview .ps-card {{ page-break-inside:avoid; break-inside:avoid; -webkit-print-color-adjust:exact; print-color-adjust:exact; box-shadow:none; }}
    #resume-preview .ps-summary {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .ps-skill {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}

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

    #resume-preview .section-header {{
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

<div id="resume-preview"><div class="page">

  <div class="ps-header">
    <div class="ps-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='ps-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="ps-contact">{contact_html}</div>
  </div>

  <div class="ps-body">
    {"<div class='ps-summary'>" + summary + "</div>" if summary else ""}
    {sec("Skills", sk_html)}
    {sec("Experience", exp_html)}
    {sec("Education", edu_html)}
    {sec("Projects", proj_html)}
    {sec("Certifications &amp; Achievements", cert_html)}
    {sec("Languages", lang_html)}
  </div>

</div></div>"""