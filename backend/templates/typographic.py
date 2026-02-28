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

    sec_count = [0]
    def sec(title, content):
        if not content.strip(): return ""
        sec_count[0] += 1
        num = str(sec_count[0]).zfill(2)
        return f"<div class='ty-section'><div class='ty-sec-head'><span class='ty-sec-num'>{num}</span><span class='ty-sec-title'>{title.upper()}</span></div>{content}</div>"

    exp_html = ""
    for e in experience:
        end  = "Present" if e.get("current") else f"{e.get('endMonth','')} {e.get('endYear','')}"
        desc = f"<div class='ty-desc'>{e.get('description','')}</div>" if e.get("description","").strip() else ""
        exp_html += f"""<div class='ty-item'>
          <div class='ty-item-head'><span class='ty-title'>{e.get('title','')}</span><span class='ty-date'>{e.get('startMonth','')} {e.get('startYear','')} &ndash; {end}</span></div>
          <div class='ty-org'>{e.get('employer','')}{' / '+e.get('location','') if e.get('location') else ''}</div>{desc}</div>"""

    edu_html = ""
    for e in education:
        gpa = f" / GPA {e.get('gpa')}" if e.get("gpa","").strip() else ""
        edu_html += f"""<div class='ty-item'>
          <div class='ty-item-head'><span class='ty-title'>{e.get('degree','')}{' &ndash; '+e.get('field','') if e.get('field') else ''}</span><span class='ty-date'>{e.get('gradYear','')}</span></div>
          <div class='ty-org'>{e.get('school','')}{', '+e.get('location','') if e.get('location') else ''}{gpa}</div></div>"""

    proj_html = ""
    for p in projects:
        parts = []
        if p.get("role","").strip():  parts.append(p.get("role"))
        if p.get("tools","").strip(): parts.append(p.get("tools"))
        sub_h  = f"<div class='ty-org'>{' &nbsp;/&nbsp; '.join(parts)}</div>" if parts else ""
        desc_h = f"<div class='ty-desc'>{p.get('description','')}</div>" if p.get("description","").strip() else ""
        url_h  = f"<div class='ty-link'><a href='{p.get('url')}' target='_blank'>{p.get('url')}</a></div>" if p.get("url","").strip() else ""
        proj_html += f"<div class='ty-item'><div class='ty-title'>{p.get('title','')}</div>{sub_h}{desc_h}{url_h}</div>"

    cert_html = ""
    for c in certifications:
        parts = []
        if c.get("issuingOrg","").strip():  parts.append(c.get("issuingOrg"))
        if c.get("achievedDate","").strip(): parts.append(c.get("achievedDate"))
        sub_h = f"<div class='ty-org'>{' / '.join(parts)}</div>" if parts else ""
        url_h = f"<a class='ty-link' href='{c.get('url')}' target='_blank'>View &rarr;</a>" if c.get("url","").strip() else ""
        cert_html += f"<div class='ty-item'><div class='ty-item-head'><span class='ty-title'>{c.get('name','')}</span>{url_h}</div>{sub_h}</div>"

    sk_html = ""
    if skills:
        sk_html = "<div class='ty-skills'>" + "".join(f"<span class='ty-skill'>{s}</span>" for s in skills if s.strip()) + "</div>"

    lv = {"Beginner":20,"Elementary":35,"Intermediate":55,"Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    lang_html = ""
    if languages:
        lang_html = "<div class='ty-lang-grid'>"
        for l in languages:
            if not l.get("name","").strip(): continue
            pct = lv.get(l.get("level","Intermediate"),55)
            lang_html += f"<div class='ty-lang'><div class='ty-lang-row'><span class='ty-lang-name'>{l.get('name','')}</span><span class='ty-lang-lv'>{l.get('level','')}</span></div><div class='ty-bar-bg'><div class='ty-bar-fill' style='width:{pct}%'></div></div></div>"
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
  #resume-preview {{ font-family:'Helvetica Neue',Arial,sans-serif; font-size:10pt; color:#111; background:#fff; line-height:1.5; }}
  #resume-preview .page {{ width:210mm; min-height:277mm; height:auto; padding:16mm 20mm; background:#fff; }}

  /* Header */
  #resume-preview .ty-header {{ margin-bottom:22px; }}
  #resume-preview .ty-header-top {{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:3px solid #111; padding-bottom:10px; margin-bottom:8px; }}
  #resume-preview .ty-name {{ font-size:28pt; font-weight:900; color:#111; text-transform:uppercase; line-height:1; letter-spacing:-0.5px; }}
  #resume-preview .ty-red {{ color:#d62828; }}
  #resume-preview .ty-profession {{ font-size:9pt; font-weight:700; text-transform:uppercase; letter-spacing:2px; color:#d62828; text-align:right; }}
  #resume-preview .ty-contact {{ font-size:8.5pt; color:#555; line-height:1.7; }}
  #resume-preview .ty-contact a {{ color:#555; text-decoration:none; }}

  /* Sections */
  #resume-preview .ty-section {{ margin-bottom:18px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .ty-sec-head {{ display:flex; align-items:baseline; gap:10px; margin-bottom:10px; border-bottom:1px solid #ddd; padding-bottom:6px; }}
  #resume-preview .ty-sec-num {{ font-size:20pt; font-weight:900; color:#d62828; line-height:1; width:38px; flex-shrink:0; }}
  #resume-preview .ty-sec-title {{ font-size:9pt; font-weight:800; letter-spacing:2.5px; color:#111; }}

  /* Items */
  #resume-preview .ty-item {{ margin-bottom:12px; page-break-inside:avoid; break-inside:avoid; padding-left:48px; }}
  #resume-preview .ty-item-head {{ display:flex; justify-content:space-between; align-items:baseline; gap:8px; }}
  #resume-preview .ty-title {{ font-weight:700; font-size:10.5pt; color:#111; }}
  #resume-preview .ty-date {{ font-size:8pt; color:#999; white-space:nowrap; font-style:italic; }}
  #resume-preview .ty-org {{ font-size:9pt; color:#666; margin-top:2px; }}
  #resume-preview .ty-desc {{ font-size:9pt; color:#333; margin-top:5px; line-height:1.55; }}
  #resume-preview .ty-link a, #resume-preview a.ty-link {{ font-size:8.5pt; color:#d62828; text-decoration:none; }}

  /* Summary */
  #resume-preview .ty-summary {{ padding-left:48px; font-size:10pt; color:#333; line-height:1.65; border-left:3px solid #d62828; margin-left:38px; padding-left:10px; }}

  /* Skills */
  #resume-preview .ty-skills {{ display:flex; flex-wrap:wrap; gap:6px; padding-left:48px; }}
  #resume-preview .ty-skill {{ font-size:9pt; padding:3px 10px; background:#111; color:#fff; font-weight:600; }}

  /* Languages */
  #resume-preview .ty-lang-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px 24px; padding-left:48px; }}
  #resume-preview .ty-lang {{ break-inside:avoid; }}
  #resume-preview .ty-lang-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
  #resume-preview .ty-lang-name {{ font-size:9.5pt; font-weight:700; }}
  #resume-preview .ty-lang-lv {{ font-size:8pt; color:#888; font-style:italic; }}
  #resume-preview .ty-bar-bg {{ height:4px; background:#eee; border-radius:0; overflow:hidden; }}
  #resume-preview .ty-bar-fill {{ height:100%; background:#d62828; }}

  @media print {{

    #resume-preview .page {{ padding:0; width:190mm; min-height: 277mm; }}
    #resume-preview .ty-section {{ page-break-inside:avoid; break-inside:avoid; }}
    #resume-preview .ty-item {{ page-break-inside:avoid; break-inside:avoid; }}
  }}
</style>

<div id="resume-preview"><div class="page">

  <div class="ty-header">
    <div class="ty-header-top">
      <div class="ty-name">{personal.get("firstName","")}<span class="ty-red">.</span>{personal.get("lastName","")}</div>
      {"<div class='ty-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    </div>
    <div class="ty-contact">{contact_html}</div>
  </div>

  {sec("Profile", f"<div class='ty-summary'>{summary}</div>") if summary else ""}
  {sec("Skills", sk_html)}
  {sec("Experience", exp_html)}
  {sec("Education", edu_html)}
  {sec("Projects", proj_html)}
  {sec("Certifications &amp; Achievements", cert_html)}
  {sec("Languages", lang_html)}

</div></div>"""