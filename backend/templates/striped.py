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

    stripe_colors = ["#f7f7f7", "#ffffff", "#f7f7f7", "#ffffff", "#f7f7f7", "#ffffff", "#f7f7f7", "#ffffff"]
    stripe_idx = [0]
    def sec(title, content):
        if not content.strip(): return ""
        bg = stripe_colors[stripe_idx[0] % len(stripe_colors)]
        stripe_idx[0] += 1
        return f"<div class='st-section' style='background:{bg}'><div class='st-inner'><div class='st-sec-label'>{title}</div><div class='st-sec-body'>{content}</div></div></div>"

    exp_html = ""
    for e in experience:
        end  = "Present" if e.get("current") else f"{e.get('endMonth','')} {e.get('endYear','')}"
        desc = f"<div class='st-desc'>{e.get('description','')}</div>" if e.get("description","").strip() else ""
        exp_html += f"""<div class='st-item'>
          <div class='st-item-date'>{e.get('startYear','')}<br><span class='st-item-date-end'>{end.split(' ')[-1] if end != 'Present' else 'Now'}</span></div>
          <div class='st-item-body'><div class='st-title'>{e.get('title','')}</div>
          <div class='st-sub'>{e.get('employer','')}{' &mdash; '+e.get('location','') if e.get('location') else ''}</div>{desc}</div></div>"""

    edu_html = ""
    for e in education:
        gpa = f" &mdash; GPA {e.get('gpa')}" if e.get("gpa","").strip() else ""
        edu_html += f"""<div class='st-item'>
          <div class='st-item-date'>{e.get('gradYear','')}</div>
          <div class='st-item-body'><div class='st-title'>{e.get('degree','')}{' &ndash; '+e.get('field','') if e.get('field') else ''}</div>
          <div class='st-sub'>{e.get('school','')}{', '+e.get('location','') if e.get('location') else ''}{gpa}</div></div></div>"""

    proj_html = ""
    for p in projects:
        parts = []
        if p.get("role","").strip():  parts.append(f"Role: {p.get('role')}")
        if p.get("tools","").strip(): parts.append(f"Tools: {p.get('tools')}")
        sub_h  = f"<div class='st-sub'>{' &nbsp;&bull;&nbsp; '.join(parts)}</div>" if parts else ""
        desc_h = f"<div class='st-desc'>{p.get('description','')}</div>" if p.get("description","").strip() else ""
        url_h  = f"<div class='st-link'><a href='{p.get('url')}' target='_blank'>{p.get('url')}</a></div>" if p.get("url","").strip() else ""
        proj_html += f"<div class='st-item'><div class='st-item-date'></div><div class='st-item-body'><div class='st-title'>{p.get('title','')}</div>{sub_h}{desc_h}{url_h}</div></div>"

    cert_html = ""
    for c in certifications:
        parts = []
        if c.get("issuingOrg","").strip():  parts.append(c.get("issuingOrg"))
        if c.get("achievedDate","").strip(): parts.append(c.get("achievedDate"))
        sub_h = f"<div class='st-sub'>{' &bull; '.join(parts)}</div>" if parts else ""
        url_h = f"<div class='st-link'><a href='{c.get('url')}' target='_blank'>View Credential</a></div>" if c.get("url","").strip() else ""
        cert_html += f"<div class='st-item'><div class='st-item-date'></div><div class='st-item-body'><div class='st-title'>{c.get('name','')}</div>{sub_h}{url_h}</div></div>"

    sk_html = ""
    if skills:
        sk_html = "<div class='st-skill-grid'>" + "".join(f"<span class='st-skill'>{s}</span>" for s in skills if s.strip()) + "</div>"

    lv = {"Beginner":20,"Elementary":35,"Intermediate":55,"Upper Intermediate":70,"Advanced":85,"Native":100,"Native / Bilingual":100}
    lang_html = ""
    if languages:
        lang_html = "<div class='st-lang-grid'>"
        for l in languages:
            if not l.get("name","").strip(): continue
            pct = lv.get(l.get("level","Intermediate"),55)
            lang_html += f"<div class='st-lang'><div class='st-lang-row'><span class='st-lang-name'>{l.get('name','')}</span><span class='st-lang-lv'>{l.get('level','')}</span></div><div class='st-bar-bg'><div class='st-bar-fill' style='width:{pct}%'></div></div></div>"
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
  #resume-preview {{ font-family:'Helvetica Neue',Arial,sans-serif; font-size:10pt; color:#1a1a1a; background:#fff; line-height:1.5; }}
  #resume-preview .page {{ width:210mm; min-height:277mm; height:auto; background:#fff; }}

  /* Header */
  #resume-preview .st-header {{ padding:18px 24px 14px 24px; background:#1a1a1a; }}
  #resume-preview .st-name {{ font-size:22pt; font-weight:800; color:#fff; text-transform:uppercase; letter-spacing:2px; line-height:1.1; }}
  #resume-preview .st-profession {{ font-size:9.5pt; color:#aaa; margin-top:4px; letter-spacing:1px; text-transform:uppercase; font-weight:300; }}
  #resume-preview .st-contact {{ font-size:8.5pt; color:#999; margin-top:8px; line-height:1.7; }}
  #resume-preview .st-contact a {{ color:#ccc; text-decoration:none; }}

  /* Striped sections */
  #resume-preview .st-section {{ width:100%; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .st-inner {{ display:flex; gap:0; padding:14px 24px; }}
  #resume-preview .st-sec-label {{ width:110px; flex-shrink:0; font-size:7.5pt; font-weight:800; text-transform:uppercase; letter-spacing:2px; color:#888; padding-top:2px; padding-right:16px; }}
  #resume-preview .st-sec-body {{ flex:1; border-left:2px solid #e0e0e0; padding-left:16px; }}

  /* Items */
  #resume-preview .st-item {{ display:flex; gap:12px; margin-bottom:11px; page-break-inside:avoid; break-inside:avoid; }}
  #resume-preview .st-item-date {{ width:38px; flex-shrink:0; font-size:8pt; font-weight:700; color:#1a1a1a; text-align:right; line-height:1.3; padding-top:1px; }}
  #resume-preview .st-item-date-end {{ font-weight:400; color:#888; }}
  #resume-preview .st-item-body {{ flex:1; border-left:1.5px solid #ddd; padding-left:10px; }}
  #resume-preview .st-title {{ font-weight:700; font-size:10pt; color:#111; }}
  #resume-preview .st-sub {{ font-size:8.5pt; color:#666; margin-top:2px; }}
  #resume-preview .st-desc {{ font-size:8.5pt; color:#444; margin-top:4px; line-height:1.5; }}
  #resume-preview .st-link a, #resume-preview a.st-link {{ font-size:8pt; color:#1a1a1a; text-decoration:underline; margin-top:2px; display:inline-block; }}

  /* Summary */
  #resume-preview .st-summary {{ font-size:9.5pt; color:#333; line-height:1.65; }}

  /* Skills */
  #resume-preview .st-skill-grid {{ display:flex; flex-wrap:wrap; gap:5px 8px; }}
  #resume-preview .st-skill {{ font-size:8.5pt; padding:3px 9px; border:1.5px solid #1a1a1a; color:#1a1a1a; font-weight:600; }}

  /* Languages */
  #resume-preview .st-lang-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:9px 24px; }}
  #resume-preview .st-lang-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
  #resume-preview .st-lang-name {{ font-size:9.5pt; font-weight:700; }}
  #resume-preview .st-lang-lv {{ font-size:8pt; color:#999; font-style:italic; }}
  #resume-preview .st-bar-bg {{ height:4px; background:#e0e0e0; border-radius:0; overflow:hidden; }}
  #resume-preview .st-bar-fill {{ height:100%; background:#1a1a1a; }}

  @media print {{

    #resume-preview .page {{ width:190mm; min-height:277mm; }}
    #resume-preview .st-header {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .st-section {{ page-break-inside:avoid; break-inside:avoid; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    #resume-preview .st-item {{ page-break-inside:avoid; break-inside:avoid; }}
  }}
</style>

<div id="resume-preview"><div class="page">

  <div class="st-header">
    <div class="st-name">{personal.get("firstName","")} {personal.get("lastName","")}</div>
    {"<div class='st-profession'>" + personal.get("profession","") + "</div>" if personal.get("profession") else ""}
    <div class="st-contact">{contact_html}</div>
  </div>

  {sec("Profile", f"<div class='st-summary'>{summary}</div>") if summary else ""}
  {sec("Skills", sk_html)}
  {sec("Experience", exp_html)}
  {sec("Education", edu_html)}
  {sec("Projects", proj_html)}
  {sec("Certifications", cert_html)}
  {sec("Languages", lang_html)}

</div></div>"""