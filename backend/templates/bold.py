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

    def sec(title, content):
        if not content.strip(): return ""
        return f"<div class='bd-section'><div class='bd-sec-head'><div class='bd-accent'></div><div class='bd-sec-title'>{title}</div></div>{content}</div>"

    exp_html = ""
    for e in experience:
        end  = "Present" if e.get("current") else f"{e.get('endMonth','')} {e.get('endYear','')}"
        desc = f"<div class='bd-desc'>{e.get('description','')}</div>" if e.get("description","").strip() else ""
        exp_html += f"""<div class='bd-item'>
          <div class='bd-item-top'><span class='bd-title'>{e.get('title','')}</span><span class='bd-badge'>{e.get('startMonth','')} {e.get('startYear','')} &ndash; {end}</span></div>
          <div class='bd-sub'>{e.get('employer','')}{' &nbsp;&bull;&nbsp; '+e.get('location','') if e.get('location') else ''}</div>{desc}</div>"""

    edu_html = ""
    for e in education:
        gpa = f" &nbsp;&bull;&nbsp; GPA {e.get('gpa')}" if e.get("gpa","").strip() else ""
        edu_html += f"""<div class='bd-item'>
          <div class='bd-item-top'><span class='bd-title'>{e.get('degree','')}{' &ndash; '+e.get('field','') if e.get('field') else ''}</span><span class='bd-badge'>{e.get('gradMonth','')} {e.get('gradYear','')}</span></div>
          <div class='bd-sub'>{e.get('school','')}{', '+e.get('location','') if e.get('location') else ''}{gpa}</div></div>"""

    proj_html = ""
    for p in projects:
        meta = []
        if p.get("role","").strip():  meta.append(f"Role: {p.get('role')}")
        if p.get("tools","").strip(): meta.append(f"Tools: {p.get('tools')}")
        sub_h = f"<div class='bd-sub'>{' &nbsp;&bull;&nbsp; '.join(meta)}</div>" if meta else ""
        desc_h = f"<div class='bd-desc'>{p.get('description','')}</div>" if p.get("description","").strip() else ""
        url_h  = f"<div class='bd-url'><a href='{p.get('url')}' target='_blank'>{p.get('url')}</a></div>" if p.get("url","").strip() else ""
        proj_html += f"<div class='bd-item'><div class='bd-title'>{p.get('title','')}</div>{sub_h}{desc_h}{url_h}</div>"

    cert_html = ""
    for c in certifications:
        meta = []
        if c.get("issuingOrg","").strip():  meta.append(c.get("issuingOrg"))
        if c.get("achievedDate","").strip(): meta.append(c.get("achievedDate"))
        sub_h = f"<div class='bd-sub'>{' &nbsp;&bull;&nbsp; '.join(meta)}</div>" if meta else ""
        url_h  = f"<a class='bd-url' href='{c.get('url')}' target='_blank'>View Credential &rarr;</a>" if c.get("url","").strip() else ""
        cert_html += f"<div class='bd-item'><div class='bd-item-top'><span class='bd-title'>{c.get('name','')}</span>{url_h}</div>{sub_h}</div>"

    sk_html = ""
    if skills:
        sk_html = "<div class='bd-skill-grid'>" + "".join(f"<div class='bd-skill'>{s}</div>" for s in skills if s.strip()) + "</div>"

    lv = {"Beginner":20,"Elementary":35,"Intermediate":55,"Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    lang_html = ""
    if languages:
        lang_html = "<div class='bd-lang-grid'>"
        for l in languages:
            if not l.get("name","").strip(): continue
            pct = lv.get(l.get("level","Intermediate"),55)
            lang_html += f"<div class='bd-lang'><div class='bd-lang-row'><span class='bd-lang-name'>{l.get('name','')}</span><span class='bd-lang-lv'>{l.get('level','')}</span></div><div class='bd-bar-bg'><div class='bd-bar-fill' style='width:{pct}%'></div></div></div>"
        lang_html += "</div>"

    websites = [w for w in personal.get("websites",[]) if w.strip()]
    c_parts = []
    if personal.get("city"):
        loc = personal.get("city")
        if personal.get("country"): loc += ", " + personal.get("country")
        c_parts.append(loc)
    if personal.get("phone"):    c_parts.append(personal.get("phone"))
    if personal.get("email"):    c_parts.append(personal.get("email"))
    if personal.get("linkedin"): c_parts.append(personal.get("linkedin"))
    for w in websites:           c_parts.append(w)
    contact_html = " &nbsp;&bull;&nbsp; ".join(c_parts)

    return f"""
<style>
  #resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}
  #resume-preview {{ font-family:'Segoe UI',Arial,sans-serif; font-size:10.5pt; color:#111; background:#fff; line-height:1.5; }}
  #resume-preview .page {{ width:210mm; background:#fff; min-height:277mm; }}

  /* Header band */
  #resume-preview .bd-header {{ background:#0d7377; padding:24px 24px 20px 24px; }}
  #resume-preview .bd-name {{ font-size:24pt; font-weight:800; color:#fff; text-transform:uppercase; letter-spacing:1px; line-height:1.1; }}
  #resume-preview .bd-profession {{ font-size:10.5pt; color:#a8e6cf; margin-top:4px; font-weight:300; letter-spacing:0.5px; }}
  #resume-preview .bd-contact {{ font-size:8.5pt; color:#c8f0e8; margin-top:10px; line-height:1.7; }}

  /* Body */
  #resume-preview .bd-body {{ padding:20px 24px; }}
  #resume-preview .bd-summary {{ font-size:10pt; color:#333; line-height:1.6; margin-bottom:18px; padding-bottom:14px; border-bottom:2px solid #0d7377; }}

  /* Section */
  #resume-preview .bd-section {{ margin-bottom:18px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .bd-sec-head {{ display:flex; align-items:center; gap:8px; margin-bottom:10px; }}
  #resume-preview .bd-accent {{ width:4px; height:18px; background:#0d7377; border-radius:2px; flex-shrink:0; }}
  #resume-preview .bd-sec-title {{ font-size:10pt; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#0d7377; }}

  /* Items */
  #resume-preview .bd-item {{ margin-bottom:12px; page-break-inside:avoid; break-inside:avoid; padding-left:12px; border-left:2px solid #e0f5f0; }}
  #resume-preview .bd-item-top {{ display:flex; justify-content:space-between; align-items:baseline; gap:8px; }}
  #resume-preview .bd-title {{ font-weight:700; font-size:10.5pt; color:#111; }}
  #resume-preview .bd-badge {{ font-size:8pt; background:#e0f5f0; color:#0d7377; padding:2px 7px; border-radius:10px; white-space:nowrap; font-weight:600; }}
  #resume-preview .bd-sub {{ font-size:9.5pt; color:#555; margin-top:2px; }}
  #resume-preview .bd-desc {{ font-size:9.5pt; color:#444; margin-top:5px; line-height:1.55; }}
  #resume-preview .bd-url a, #resume-preview a.bd-url {{ font-size:8.5pt; color:#0d7377; text-decoration:none; margin-top:3px; display:inline-block; }}

  /* Skills */
  #resume-preview .bd-skill-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:6px; }}
  #resume-preview .bd-skill {{ background:#f0faf8; border:1px solid #b2e0d8; color:#0d7377; font-size:9pt; padding:4px 8px; border-radius:3px; font-weight:600; text-align:center; }}

  /* Languages */
  #resume-preview .bd-lang-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px 24px; }}
  #resume-preview .bd-lang {{ break-inside:avoid; }}
  #resume-preview .bd-lang-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
  #resume-preview .bd-lang-name {{ font-size:9.5pt; font-weight:700; }}
  #resume-preview .bd-lang-lv {{ font-size:8pt; color:#888; font-style:italic; }}
  #resume-preview .bd-bar-bg {{ height:4px; background:#e0f5f0; border-radius:2px; overflow:hidden; }}
  #resume-preview .bd-bar-fill {{ height:100%; background:#0d7377; border-radius:2px; }}

  @media print {{
    #resume-preview .page {{ width:190mm; min-height:277mm; margin:0; padding:0; }}
    #resume-preview .bd-section {{ page-break-inside:avoid; break-inside:avoid; }}
    #resume-preview .bd-item {{ page-break-inside:avoid; break-inside:avoid; }}
  }}
</style>

<div id="resume-preview"><div class="page">

  <div class="bd-header">
    <div class="bd-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='bd-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="bd-contact">{contact_html}</div>
  </div>

  <div class="bd-body">
    {"<div class='bd-summary'>" + summary + "</div>" if summary else ""}
    {sec("Skills", sk_html)}
    {sec("Professional Experience", exp_html)}
    {sec("Education", edu_html)}
    {sec("Projects", proj_html)}
    {sec("Certifications &amp; Achievements", cert_html)}
    {sec("Languages", lang_html)}
  </div>

</div></div>"""