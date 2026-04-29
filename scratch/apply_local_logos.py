#!/usr/bin/env python3
"""
apply_local_logos.py — Replace ALL external logo URLs (cdn.simpleicons.org,
api.iconify.design, wikimedia) with relative paths to cursos/logos/*.svg
"""
import os, re

BASE = "/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos"
LOGOS_DIR = os.path.join(BASE, "logos")

# Map: partial URL fragment → local filename
# Ordered from most specific to least specific
URL_MAP = {
    # SimpleIcons CDN
    "simpleicons.org/html5":        "html5.svg",
    "simpleicons.org/css3":         "css3.svg",
    "simpleicons.org/javascript":   "javascript.svg",
    "simpleicons.org/figma":        "figma.svg",
    "simpleicons.org/wordpress":    "wordpress.svg",
    "simpleicons.org/googlechrome": "chrome.svg",
    "simpleicons.org/linux":        "linux.svg",
    "simpleicons.org/ubuntu":       "ubuntu.svg",
    "simpleicons.org/linkedin":     "linkedin.svg",
    "simpleicons.org/trello":       "trello.svg",
    "simpleicons.org/autocad":      "autocad.svg",
    "simpleicons.org/autodesk":     "autodesk.svg",
    "simpleicons.org/arduino":      "arduino.svg",
    "simpleicons.org/samsung":      "samsung.svg",
    "simpleicons.org/cisco":        "cisco.svg",
    "simpleicons.org/virtualbox":   "virtualbox.svg",
    "simpleicons.org/sap":          "sap.svg",
    "simpleicons.org/googlemaps":   "googlemaps.svg",
    # Iconify — these might come from previous attempts or inline fixes
    "iconify.design/skill-icons/windows": "windows.svg",
    "iconify.design/vscode-icons/file-type-word": "word.svg",
    "iconify.design/vscode-icons/file-type-excel": "excel.svg",
    "iconify.design/vscode-icons/file-type-powerpoint": "powerpoint.svg",
    "iconify.design/vscode-icons/file-type-outlook": "outlook.svg",
    "iconify.design/logos/microsoft-teams": "teams.svg",
    "iconify.design/simple-icons/powerbi": "powerbi.svg",
    "iconify.design/vscode-icons/file-type-vscode": "vscode.svg",
    "iconify.design/logos/linux-tux": "linux.svg",
    "iconify.design/logos/sap": "sap.svg",
    "iconify.design/logos/google-maps": "googlemaps.svg",
    "iconify.design/logos/css-3": "css3.svg",
    "iconify.design/logos/linkedin-icon": "linkedin.svg",
    "iconify.design/simple-icons/cisco": "cisco.svg",
    "iconify.design/simple-icons/virtualbox": "virtualbox.svg",
    "iconify.design/simple-icons/autocad": "autocad.svg",
    "iconify.design/simple-icons/siemens": "siemens.svg",
    "iconify.design/simple-icons/googlechrome": "chrome.svg",
    "iconify.design/simple-icons/lg": "lg.svg",
    "iconify.design/simple-icons/schneiderelectric": "schneider.svg",
    "iconify.design/simple-icons/arduino": "arduino.svg",
    "iconify.design/simple-icons/freecad": "freecad.svg",
    "iconify.design/simple-icons/ubuntu": "ubuntu.svg",
    "iconify.design/logos/visual-studio-code": "vscode.svg",
    # Wikimedia
    "Windows_logo_-_2021.svg":      "windows.svg",
    "Visual_Studio_Code_1.35_icon": "vscode.svg",
    "New_Power_BI_Logo":            "powerbi.svg",
    "Microsoft_Power_BI_Logo":      "powerbi.svg",
    "Office_Word":                  "word.svg",
    "Office_Excel":                 "excel.svg",
    "Office_PowerPoint":            "powerpoint.svg",
    "Office_Outlook":               "outlook.svg",
    "Office_Teams":                 "teams.svg",
}

def replace_img_src(html, url_frag, local_file):
    """Replace <img src="URL containing url_frag"> with local path."""
    # Match the full img tag with src containing our fragment
    pattern = r'<img\b([^>]*?)src="[^"]*' + re.escape(url_frag) + r'[^"]*"([^>]*)>'
    def do_replace(m):
        before = m.group(1)
        after = m.group(2)
        # Remove any old alt that might already be there, build clean tag
        before = re.sub(r'\salt="[^"]*"', '', before)
        after  = re.sub(r'\salt="[^"]*"', '', after)
        # Try to extract alt from alt attribute in either side
        alt_m = re.search(r'alt="([^"]*)"', m.group(0))
        alt = alt_m.group(1) if alt_m else local_file.replace('.svg','')
        return f'<img{before}src="logos/{local_file}" alt="{alt}"{after}>'
    return re.subn(pattern, do_replace, html)

HTML_FILES = sorted(f for f in os.listdir(BASE) if f.endswith('.html'))
total = 0

for filename in HTML_FILES:
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    file_count = 0
    for frag, local in URL_MAP.items():
        if frag in html:
            html, n = replace_img_src(html, frag, local)
            file_count += n
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {filename}: {file_count} URL→local replacement(s)")
        total += file_count
    else:
        print(f"   {filename}: no changes")

print(f"\nTotal: {total} replacements across {len(HTML_FILES)} files")
