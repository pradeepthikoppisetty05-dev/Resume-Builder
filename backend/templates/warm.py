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

    def main_sec(title, content):
        if not content.strip(): return ""
        return f"<div class='wm-section'><div class='wm-sec-title'>{title}</div>{content}</div>"

    def side_sec(title, content):
        if not content.strip(): return ""
        return f"<div class='wm-side-section'><div class='wm-side-title'>{title}</div>{content}</div>"

    exp_html = ""
    for e in experience:
        end  = "Present" if e.get("current") else f"{e.get('endMonth','')} {e.get('endYear','')}"
        desc = f"<div class='wm-desc'>{e.get('description','')}</div>" if e.get("description","").strip() else ""
        exp_html += f"""<div class='wm-item'>
          <div class='wm-item-row'><span class='wm-title'>{e.get('title','')}</span><span class='wm-date'>{e.get('startMonth','')} {e.get('startYear','')} &ndash; {end}</span></div>
          <div class='wm-sub'>{e.get('employer','')}{' &middot; '+e.get('location','') if e.get('location') else ''}</div>{desc}</div>"""

    edu_html = ""
    for e in education:
        gpa = f" &middot; GPA {e.get('gpa')}" if e.get("gpa","").strip() else ""
        edu_html += f"""<div class='wm-item'>
          <div class='wm-item-row'><span class='wm-title'>{e.get('degree','')}{' &ndash; '+e.get('field','') if e.get('field') else ''}</span><span class='wm-date'>{e.get('gradMonth','')} {e.get('gradYear','')}</span></div>
          <div class='wm-sub'>{e.get('school','')}{', '+e.get('location','') if e.get('location') else ''}{gpa}</div></div>"""

    proj_html = ""
    for p in projects:
        parts = []
        if p.get("role","").strip():  parts.append(f"<strong>Role:</strong> {p.get('role')}")
        if p.get("tools","").strip(): parts.append(f"<strong>Tools:</strong> {p.get('tools')}")
        sub_h  = f"<div class='wm-sub'>{' &nbsp;&bull;&nbsp; '.join(parts)}</div>" if parts else ""
        desc_h = f"<div class='wm-desc'>{p.get('description','')}</div>" if p.get("description","").strip() else ""
        url_h  = f"<a class='wm-link' href='{p.get('url')}' target='_blank'>{p.get('url')}</a>" if p.get("url","").strip() else ""
        proj_html += f"<div class='wm-item'><div class='wm-title'>{p.get('title','')}</div>{sub_h}{desc_h}{url_h}</div>"

    # Sidebar: skills, certs, languages
    sk_side = ""
    if skills:
        sk_side = "<ul class='wm-skill-list'>" + "".join(f"<li>{s}</li>" for s in skills if s.strip()) + "</ul>"

    cert_side = ""
    for c in certifications:
        meta = []
        if c.get("issuingOrg","").strip():  meta.append(c.get("issuingOrg"))
        if c.get("achievedDate","").strip(): meta.append(c.get("achievedDate"))
        sub_h = f"<div class='wm-side-sub'>{' &bull; '.join(meta)}</div>" if meta else ""
        url_h = f"<a class='wm-side-link' href='{c.get('url')}' target='_blank'>View &rarr;</a>" if c.get("url","").strip() else ""
        cert_side += f"<div class='wm-side-item'><div class='wm-side-item-title'>{c.get('name','')}</div>{sub_h}{url_h}</div>"

    lv = {"Beginner":20,"Elementary":35,"Intermediate":55,"Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    lang_side = ""
    if languages:
        lang_side = "<div class='wm-lang-list'>"
        for l in languages:
            if not l.get("name","").strip(): continue
            pct = lv.get(l.get("level","Intermediate"),55)
            lang_side += f"<div class='wm-lang'><div class='wm-lang-row'><span class='wm-lang-name'>{l.get('name','')}</span><span class='wm-lang-lv'>{l.get('level','')}</span></div><div class='wm-bar-bg'><div class='wm-bar-fill' style='width:{pct}%'></div></div></div>"
        lang_side += "</div>"

    websites = [w for w in personal.get("websites",[]) if w.strip()]
    contact_lines = []
    if personal.get("city"):
        loc = personal.get("city")
        if personal.get("country"): loc += ", " + personal.get("country")
        contact_lines.append(loc)
    if personal.get("phone"):    contact_lines.append(personal.get("phone"))
    if personal.get("email"):    contact_lines.append(personal.get("email"))
    if personal.get("linkedin"): contact_lines.append(personal.get("linkedin"))
    for w in websites:           contact_lines.append(w)

    return f"""
<style>
  #resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}
  #resume-preview {{ font-family:'Georgia',serif; font-size:10pt; color:#2c1a0e; background:#fff; line-height:1.55; }}
  #resume-preview .page {{ width:210mm; min-height:277mm; height:auto; display:flex; background:#faf7f4; }}

  /* Left colour strip */
  #resume-preview .wm-strip {{ width:8px; background:#c1440e; flex-shrink:0; }}

  /* Sidebar */
  #resume-preview .wm-sidebar {{ width:33%; background:#f0ebe3; padding:22px 16px 22px 16px; flex-shrink:0; }}
  #resume-preview .wm-side-name {{ font-size:15pt; font-weight:700; color:#2c1a0e; line-height:1.2; word-break:break-word; font-style:italic; }}
  #resume-preview .wm-side-prof {{ font-size:9pt; color:#c1440e; margin-top:4px; font-style:normal; font-weight:700; letter-spacing:0.3px; }}
  #resume-preview .wm-contact {{ margin-top:14px; padding-bottom:14px; border-bottom:1px solid #d9cfc4; margin-bottom:18px; }}
  #resume-preview .wm-contact-item {{ font-size:8pt; color:#6b4c36; margin-bottom:4px; line-height:1.4; word-break:break-all; }}
  #resume-preview .wm-side-section {{ margin-bottom:18px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .wm-side-title {{ font-size:7.5pt; font-weight:700; text-transform:uppercase; letter-spacing:2px; color:#c1440e; margin-bottom:8px; padding-bottom:4px; border-bottom:1px solid #d9cfc4; }}
  #resume-preview .wm-skill-list {{ list-style:none; }}
  #resume-preview .wm-skill-list li {{ font-size:9pt; color:#3d2010; padding:3px 0; border-bottom:1px dotted #d9cfc4; }}
  #resume-preview .wm-side-item {{ margin-bottom:9px; }}
  #resume-preview .wm-side-item-title {{ font-size:9pt; font-weight:700; color:#2c1a0e; }}
  #resume-preview .wm-side-sub {{ font-size:8pt; color:#8a6650; margin-top:1px; }}
  #resume-preview .wm-side-link {{ font-size:8pt; color:#c1440e; text-decoration:none; }}
  #resume-preview .wm-lang-list {{ display:flex; flex-direction:column; gap:9px; }}
  #resume-preview .wm-lang-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
  #resume-preview .wm-lang-name {{ font-size:9pt; font-weight:700; color:#2c1a0e; }}
  #resume-preview .wm-lang-lv {{ font-size:7.5pt; color:#8a6650; font-style:italic; }}
  #resume-preview .wm-bar-bg {{ height:3px; background:#d9cfc4; border-radius:2px; overflow:hidden; }}
  #resume-preview .wm-bar-fill {{ height:100%; background:#c1440e; border-radius:2px; }}

  /* Main content */
  #resume-preview .wm-main {{ flex:1; padding:22px 20px; background:#fff; }}
  #resume-preview .wm-summary {{ font-size:9.5pt; color:#3d2010; line-height:1.7; margin-bottom:18px; padding-bottom:14px; border-bottom:1.5px solid #c1440e; font-style:italic; }}
  #resume-preview .wm-section {{ margin-bottom:18px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .wm-sec-title {{ font-size:9pt; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:#c1440e; margin-bottom:8px; padding-bottom:4px; border-bottom:1.5px solid #f0ebe3; }}
  #resume-preview .wm-item {{ margin-bottom:13px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .wm-item-row {{ display:flex; justify-content:space-between; align-items:baseline; gap:8px; }}
  #resume-preview .wm-title {{ font-weight:700; font-size:10.5pt; color:#2c1a0e; }}
  #resume-preview .wm-date {{ font-size:8pt; color:#8a6650; white-space:nowrap; font-style:italic; }}
  #resume-preview .wm-sub {{ font-size:9pt; color:#6b4c36; margin-top:2px; font-style:italic; }}
  #resume-preview .wm-desc {{ font-size:9pt; color:#3d2010; margin-top:5px; line-height:1.55; font-style:normal; }}
  #resume-preview .wm-link {{ font-size:8.5pt; color:#c1440e; text-decoration:none; margin-top:3px; display:inline-block; }}

  @media print {{

    #resume-preview .page {{ width:190mm; min-height:277mm; display:flex; }}
    #resume-preview .wm-strip {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .wm-sidebar {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .wm-section {{ page-break-inside:avoid; break-inside:avoid; }}
    #resume-preview .wm-item {{ page-break-inside:avoid; break-inside:avoid; }}
    #resume-preview .wm-side-section {{ page-break-inside:avoid; break-inside:avoid; }}
  }}
</style>

<div id="resume-preview"><div class="page">

  <div class="wm-strip"></div>

  <div class="wm-sidebar">
    <div class="wm-side-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='wm-side-prof'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="wm-contact">
      {"".join(f"<div class='wm-contact-item'>{c}</div>" for c in contact_lines)}
    </div>
    {side_sec("Skills", sk_side)}
    {side_sec("Languages", lang_side)}
    {side_sec("Certifications &amp; Achievements", cert_side)}
  </div>

  <div class="wm-main">
    {"<div class='wm-summary'>" + summary + "</div>" if summary else ""}
    {main_sec("Experience", exp_html)}
    {main_sec("Education", edu_html)}
    {main_sec("Projects", proj_html)}
  </div>

</div></div>"""