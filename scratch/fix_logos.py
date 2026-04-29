#!/usr/bin/env python3
"""
fix_logos.py — Replace broken external logo <img> tags with reliable inline SVGs
across all course HTML pages.
"""
import os, re

BASE = "/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos"

# Each entry: (pattern_in_src, replacement_img_tag)
# We use full <img ...> patterns so we can replace the whole tag.

WINDOWS_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4875 4875" style="width:100%;height:100%;"><path fill="#0078d4" d="M0 0h2311v2310H0zm2564 0h2311v2310H2564zM0 2564h2311v2311H0zm2564 0h2311v2311H2564"/></svg>'

WORD_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="width:100%;height:100%;"><rect width="48" height="48" rx="4" fill="#185ABD"/><path fill="#fff" d="M12 12h6v24h-6zm8 0l4 9 4-9h4L26 24l6 12h-4l-4-9-4 9h-4l6-12-6-12z"/></svg>'

EXCEL_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="width:100%;height:100%;"><rect width="48" height="48" rx="4" fill="#107C41"/><path fill="#fff" d="M12 12h6v24h-6zm6 0h18v6H18zm0 8h18v4H18zm0 6h18v4H18zm0 6h18v4H18z"/><path fill="rgba(255,255,255,0.3)" d="M14 14l8 10-8 10h4l6-10-6-10z"/></svg>'

PPT_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="width:100%;height:100%;"><rect width="48" height="48" rx="4" fill="#C43E1C"/><path fill="#fff" d="M12 12h14c4.4 0 8 3.6 8 8s-3.6 8-8 8H18v8h-6V12zm6 4v8h8c2.2 0 4-1.8 4-4s-1.8-4-4-4h-8z"/></svg>'

OUTLOOK_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="width:100%;height:100%;"><rect width="48" height="48" rx="4" fill="#0F6CBD"/><ellipse cx="22" cy="24" rx="8" ry="10" fill="none" stroke="#fff" stroke-width="3"/><rect x="28" y="14" width="10" height="20" rx="2" fill="#50E6FF" opacity=".7"/><line x1="28" y1="26" x2="38" y2="26" stroke="#fff" stroke-width="2"/></svg>'

TEAMS_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="width:100%;height:100%;"><rect width="48" height="48" rx="4" fill="#4B53BC"/><circle cx="30" cy="18" r="5" fill="#fff"/><circle cx="18" cy="20" r="4" fill="#fff" opacity=".8"/><path fill="#fff" d="M30 26c4 0 10 2 10 5v3H20v-3c0-3 6-5 10-5z"/><path fill="#fff" opacity=".7" d="M18 28c-4 0-8 1.6-8 4v2h10v-2c0-1.5.6-2.9 1.6-4H18z"/></svg>'

VSCODE_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width:100%;height:100%;"><path d="M74.9 20.1L50 44.6 26.9 25.5 20 29.3v41.5l6.9 3.9L50 55.6l25 19.1 6.9-3.9V29.3z" fill="#0065A9"/><path d="M74.9 79.9L50 60.8 26.9 79.9 20 76V29.3l6.9-3.9L50 44.6l25-19.2 6.9 3.9V76z" fill="#007ACC"/><path d="M74.9 79.9L50 60.8V44.6l24.9-24.5 5.1 5.9v48z" fill="#1F9CF0"/><path d="M26.9 74.5L50 55.4V44.6L26.9 25.5 20 29.3v41.4z" fill="rgba(0,0,0,0.25)"/></svg>'

POWERBI_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" style="width:100%;height:100%;"><rect x="6" y="4" width="4" height="24" fill="#F2C811"/><rect x="12" y="10" width="4" height="18" fill="#F2C811" opacity=".85"/><rect x="18" y="16" width="4" height="12" fill="#F2C811" opacity=".7"/><rect x="24" y="8" width="4" height="20" fill="#F2C811" opacity=".92"/></svg>'

# Mapping: partial URL match → inline SVG string
REPLACEMENTS = {
    "Windows_logo_-_2021.svg": WINDOWS_SVG,
    "Word_%282019": WORD_SVG,
    "Excel_%282019": EXCEL_SVG,
    "PowerPoint_%282019": PPT_SVG,
    "Outlook_%282018": OUTLOOK_SVG,
    "Teams_%282019": TEAMS_SVG,
    "Visual_Studio_Code_1.35_icon.svg": VSCODE_SVG,
    "New_Power_BI_Logo.svg": POWERBI_SVG,
    "Microsoft_Power_BI_Logo.svg": POWERBI_SVG,
}

def replace_img_tag(html, url_fragment, svg_content):
    """Replace <img src="...URL_FRAGMENT..."> with an inline SVG wrapper."""
    pattern = r'<img\s+src="[^"]*' + re.escape(url_fragment) + r'[^"]*"[^>]*>'
    replacement = svg_content
    new_html, count = re.subn(pattern, replacement, html)
    return new_html, count

files = [f for f in os.listdir(BASE) if f.endswith('.html')]
total_replacements = 0

for filename in sorted(files):
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    file_replacements = 0
    
    for url_frag, svg in REPLACEMENTS.items():
        if url_frag in html:
            html, count = replace_img_tag(html, url_frag, svg)
            file_replacements += count
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {filename}: {file_replacements} replacement(s)")
        total_replacements += file_replacements
    else:
        print(f"   {filename}: nothing to change")

print(f"\nTotal: {total_replacements} replacement(s) across {len(files)} files")
