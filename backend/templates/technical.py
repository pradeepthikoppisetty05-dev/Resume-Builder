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
        slug = title.upper().replace(" ","_").replace("&AMP;","AND")
        return f"<div class='tc-section'><div class='tc-sec-head'><span class='tc-comment'>/* {slug} */</span></div>{content}</div>"

    exp_html = ""
    for e in experience:
        end  = "Present" if e.get("current") else f"{e.get('endMonth','')} {e.get('endYear','')}"
        desc = f"<div class='tc-desc'>{e.get('description','')}</div>" if e.get("description","").strip() else ""
        exp_html += f"""<div class='tc-item'>
          <div class='tc-item-row'><span class='tc-prompt'>&gt;&gt;</span><span class='tc-title'>{e.get('title','')}</span><span class='tc-date'>[{e.get('startYear','')} &mdash; {end.split(' ')[-1] if end != 'Present' else 'now'}]</span></div>
          <div class='tc-sub'><span class='tc-key'>employer:</span> {e.get('employer','')}{' | '+e.get('location','') if e.get('location') else ''}</div>{desc}</div>"""

    edu_html = ""
    for e in education:
        gpa = f" | GPA: {e.get('gpa')}" if e.get("gpa","").strip() else ""
        edu_html += f"""<div class='tc-item'>
          <div class='tc-item-row'><span class='tc-prompt'>&gt;&gt;</span><span class='tc-title'>{e.get('degree','')}{' :: '+e.get('field','') if e.get('field') else ''}</span><span class='tc-date'>[{e.get('gradYear','') }]</span></div>
          <div class='tc-sub'><span class='tc-key'>institution:</span> {e.get('school','')}{', '+e.get('location','') if e.get('location') else ''}{gpa}</div></div>"""

    proj_html = ""
    for p in projects:
        lines = []
        if p.get("role","").strip():  lines.append(f"<div class='tc-sub'><span class='tc-key'>role:</span> {p.get('role')}</div>")
        if p.get("tools","").strip(): lines.append(f"<div class='tc-sub'><span class='tc-key'>stack:</span> {p.get('tools')}</div>")
        desc_h = f"<div class='tc-desc'>{p.get('description','')}</div>" if p.get("description","").strip() else ""
        url_h  = f"<div class='tc-sub'><span class='tc-key'>url:</span> <a href='{p.get('url')}' target='_blank'>{p.get('url')}</a></div>" if p.get("url","").strip() else ""
        proj_html += f"<div class='tc-item'><div class='tc-item-row'><span class='tc-prompt'>&gt;&gt;</span><span class='tc-title'>{p.get('title','')}</span></div>{''.join(lines)}{desc_h}{url_h}</div>"

    cert_html = ""
    for c in certifications:
        lines = []
        if c.get("issuingOrg","").strip():  lines.append(f"<div class='tc-sub'><span class='tc-key'>issuer:</span> {c.get('issuingOrg')}</div>")
        if c.get("achievedDate","").strip(): lines.append(f"<div class='tc-sub'><span class='tc-key'>date:</span> {c.get('achievedDate')}</div>")
        url_h = f"<div class='tc-sub'><span class='tc-key'>url:</span> <a href='{c.get('url')}' target='_blank'>{c.get('url')}</a></div>" if c.get("url","").strip() else ""
        cert_html += f"<div class='tc-item'><div class='tc-item-row'><span class='tc-prompt'>&gt;&gt;</span><span class='tc-title'>{c.get('name','')}</span></div>{''.join(lines)}{url_h}</div>"

    sk_html = ""
    if skills:
        filtered = [s for s in skills if s.strip()]
        rows = [filtered[i:i+4] for i in range(0, len(filtered), 4)]
        sk_html = "<div class='tc-skill-block'>"
        for row in rows:
            sk_html += "<div class='tc-skill-row'>" + "".join(f"<span class='tc-skill'>'{s}'</span>" for s in row) + "</div>"
        sk_html += "</div>"

    lv = {"Beginner":20,"Elementary":35,"Intermediate":55,"Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    lang_html = ""
    if languages:
        lang_html = "<div class='tc-lang-block'>"
        for l in languages:
            if not l.get("name","").strip(): continue
            pct = lv.get(l.get("level","Intermediate"),55)
            lang_html += f"<div class='tc-lang-row'><span class='tc-key'>{l.get('name','')}</span><div class='tc-bar-wrap'><div class='tc-bar-fill' style='width:{pct}%'></div></div><span class='tc-lang-lv'>{l.get('level','')}</span></div>"
        lang_html += "</div>"

    websites = [w for w in personal.get("websites",[]) if w.strip()]
    c_parts = []
    if personal.get("city"):
        loc = personal.get("city")
        if personal.get("country"): loc += ", " + personal.get("country")
        c_parts.append(f"location: {loc}")
    if personal.get("phone"):    c_parts.append(f"tel: {personal.get('phone')}")
    if personal.get("email"):    c_parts.append(f'email: <a href="mailto:{personal.get("email")}">{personal.get("email")}</a>')
    if personal.get("linkedin"): c_parts.append(f'web: <a href="{personal.get("linkedin")}" target="_blank">{personal.get("linkedin")}</a>')
    for w in websites:           c_parts.append(f'web: <a href="{w}" target="_blank">{w}</a>')
    contact_html = " &nbsp;|&nbsp; ".join(c_parts)

    return f"""
<style>
  #resume-preview * {{ margin:0; padding:0; box-sizing:border-box; }}
  #resume-preview {{ font-family:'Courier New',Courier,monospace; font-size:9.5pt; color:#1a1a1a; background:#fff; line-height:1.55; }}
  #resume-preview .page {{ width:210mm; min-height:277mm; height:auto; background:#fff; }}

  /* Terminal header */
  #resume-preview .tc-header {{ background:#0d1117; padding:20px 22px; }}
  #resume-preview .tc-header-bar {{ font-size:8pt; color:#555; margin-bottom:10px; letter-spacing:1px; }}
  #resume-preview .tc-header-bar span {{ color:#3fb950; }}
  #resume-preview .tc-name {{ font-size:18pt; font-weight:700; color:#3fb950; letter-spacing:2px; }}
  #resume-preview .tc-profession {{ font-size:9pt; color:#8b949e; margin-top:4px; }}
  #resume-preview .tc-contact {{ font-size:10pt; color:#6e7681; margin-top:10px; line-height:1.7; }}
  #resume-preview .tc-contact a {{ color:#58a6ff; text-decoration:none; }}

  /* Body */
  #resume-preview .tc-body {{ padding:16px 22px; background:#fff; }}

  /* Summary */
  #resume-preview .tc-summary {{ font-size:10pt; color:#333; line-height:1.6; padding:8px 12px; background:#f6f8fa; border-left:3px solid #3fb950; margin-bottom:14px; }}

  /* Sections */
  #resume-preview .tc-section {{ margin-bottom:16px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .tc-sec-head {{ margin-bottom:8px; }}
  #resume-preview .tc-comment {{ font-size:9pt; font-weight:700; color:#6a737d; letter-spacing:0.5px; }}

  /* Items */
  #resume-preview .tc-item {{ margin-bottom:11px; padding-left:4px; page-break-inside:avoid; break-inside:avoid; border-left:2px solid #e1e4e8; padding-left:10px; margin-left:4px; }}
  #resume-preview .tc-item-row {{ display:flex; align-items:baseline; gap:8px; margin-bottom:2px; }}
  #resume-preview .tc-prompt {{ color:#3fb950; font-weight:700; font-size:9pt; flex-shrink:0; }}
  #resume-preview .tc-title {{ font-weight:700; font-size:10pt; color:#111; }}
  #resume-preview .tc-date {{ font-size:8pt; color:#999; margin-left:auto; white-space:nowrap; }}
  #resume-preview .tc-key {{ color:#6a737d; font-size:8.5pt; }}
  #resume-preview .tc-sub {{ font-size:8.5pt; color:#444; margin-top:2px; }}
  #resume-preview .tc-sub a {{ color:#58a6ff; text-decoration:none; }}
  #resume-preview .tc-desc {{ font-size:8.5pt; color:#333; margin-top:4px; line-height:1.5; }}

  /* Skills */
  #resume-preview .tc-skill-block {{ font-size:9pt; }}
  #resume-preview .tc-skill-row {{ display:flex; flex-wrap:wrap; gap:4px 10px; margin-bottom:4px; }}
  #resume-preview .tc-skill {{ color:#1a7a4a; background:#f0fff4; padding:2px 6px; border:1px solid #c3e6cb; border-radius:2px; }}

  /* Languages */
  #resume-preview .tc-lang-block {{ display:flex; flex-direction:column; gap:7px; }}
  #resume-preview .tc-lang-row {{ display:flex; align-items:center; gap:10px; }}
  #resume-preview .tc-lang-row .tc-key {{ width:80px; flex-shrink:0; font-size:9pt; }}
  #resume-preview .tc-bar-wrap {{ flex:1; height:6px; background:#e1e4e8; border-radius:2px; overflow:hidden; }}
  #resume-preview .tc-bar-fill {{ height:100%; background:#3fb950; border-radius:2px; }}
  #resume-preview .tc-lang-lv {{ font-size:8pt; color:#6a737d; width:110px; flex-shrink:0; }}

  @media print {{

    #resume-preview .page {{ width:190mm; min-height:277mm; }}
    #resume-preview .tc-header {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .tc-section {{ page-break-inside:avoid; break-inside:avoid; }}
    #resume-preview .tc-item {{ page-break-inside:avoid; break-inside:avoid; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .tc-skill {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .tc-summary {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  }}
</style>

<div id="resume-preview"><div class="page">

  <div class="tc-header">
    <div class="tc-header-bar">resume.json &nbsp;<span>&#x2713; parsed successfully</span></div>
    <div class="tc-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='tc-profession'>// " + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="tc-contact">{contact_html}</div>
  </div>

  <div class="tc-body">
    {"<div class='tc-summary'>" + summary + "</div>" if summary else ""}
    {sec("Skills", sk_html)}
    {sec("Experience", exp_html)}
    {sec("Education", edu_html)}
    {sec("Projects", proj_html)}
    {sec("Certifications &amp; Achievements", cert_html)}
    {sec("Languages", lang_html)}
  </div>

</div></div>"""