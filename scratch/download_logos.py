#!/usr/bin/env python3
"""
download_logos.py — Download all real, official brand SVGs to cursos/logos/
then update all HTML files to use local paths.
"""
import os, re, urllib.request, urllib.error, time

BASE = "/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos"
LOGOS_DIR = os.path.join(BASE, "logos")
os.makedirs(LOGOS_DIR, exist_ok=True)

# Map: local filename → best working URL
LOGO_SOURCES = {
    # ── Microsoft (via vscode-icons which has real colored Office icons) ──
    "windows.svg":      "https://api.iconify.design/skill-icons/windows-dark.svg",
    "word.svg":         "https://api.iconify.design/vscode-icons/file-type-word.svg",
    "excel.svg":        "https://api.iconify.design/vscode-icons/file-type-excel.svg",
    "powerpoint.svg":   "https://api.iconify.design/vscode-icons/file-type-powerpoint.svg",
    "outlook.svg":      "https://api.iconify.design/vscode-icons/file-type-outlook.svg",
    "teams.svg":        "https://api.iconify.design/logos/microsoft-teams.svg",
    "powerbi.svg":      "https://api.iconify.design/simple-icons/powerbi.svg?color=%23F2C811",
    "vscode.svg":       "https://api.iconify.design/vscode-icons/file-type-vscode.svg",

    # ── Web ──
    "html5.svg":        "https://cdn.simpleicons.org/html5",
    "css3.svg":         "https://cdn.simpleicons.org/css3",
    "javascript.svg":   "https://cdn.simpleicons.org/javascript",
    "figma.svg":        "https://cdn.simpleicons.org/figma",
    "wordpress.svg":    "https://cdn.simpleicons.org/wordpress",
    "chrome.svg":       "https://api.iconify.design/logos/chrome.svg",

    # ── IT & Networks ──
    "linux.svg":        "https://api.iconify.design/logos/linux-tux.svg",
    "ubuntu.svg":       "https://cdn.simpleicons.org/ubuntu",
    "cisco.svg":        "https://api.iconify.design/simple-icons/cisco.svg?color=%231BA0D7",
    "virtualbox.svg":   "https://api.iconify.design/simple-icons/virtualbox.svg?color=%23183A61",

    # ── Business ──
    "linkedin.svg":     "https://cdn.simpleicons.org/linkedin",
    "trello.svg":       "https://cdn.simpleicons.org/trello",
    "sap.svg":          "https://api.iconify.design/logos/sap.svg",
    "googlemaps.svg":   "https://api.iconify.design/logos/google-maps.svg",

    # ── Engineering / CAD ──
    "autocad.svg":      "https://api.iconify.design/simple-icons/autocad.svg?color=%23E51937",
    "autodesk.svg":     "https://cdn.simpleicons.org/autodesk",
    "siemens.svg":      "https://api.iconify.design/simple-icons/siemens.svg?color=%23009999",
    "schneider.svg":    "https://api.iconify.design/simple-icons/schneiderelectric.svg?color=%233DCD58",
    "arduino.svg":      "https://cdn.simpleicons.org/arduino",
    "freecad.svg":      "https://api.iconify.design/simple-icons/freecad.svg?color=%23FC0",

    # ── Appliances ──
    "samsung.svg":      "https://cdn.simpleicons.org/samsung",
    "lg.svg":           "https://api.iconify.design/simple-icons/lg.svg?color=%23A50034",
}

def download(local_name, url):
    dest = os.path.join(LOGOS_DIR, local_name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
        with open(dest, "wb") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  ⚠️  Failed: {url} → {e}")
        return False

print("Downloading logos…")
for name, url in LOGO_SOURCES.items():
    ok = download(name, url)
    mark = "✅" if ok else "❌"
    print(f"{mark} {name}")
    time.sleep(0.1)  # be polite

print(f"\nDone. Logos saved to {LOGOS_DIR}/")

# ── Now define the mapping: SVG patterns in HTML → local file ──
HTML_FILES = [f for f in os.listdir(BASE) if f.endswith('.html')]

# Map: string to find anywhere in <img src="...">  OR inline SVG → local file
# After this we'll do a more targeted replacement.
IMG_REPLACEMENTS = {
    # Microsoft — was inline SVG / old wikimedia
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>Windows)':
        ('windows.svg', 'Windows'),
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>Microsoft Word)':
        ('word.svg', 'Microsoft Word'),
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>Microsoft Excel)':
        ('excel.svg', 'Microsoft Excel'),
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>(?:Microsoft Power[Pp]oint|PowerPoint))':
        ('powerpoint.svg', 'PowerPoint'),
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>(?:Outlook|Microsoft Outlook))':
        ('outlook.svg', 'Outlook'),
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>Microsoft Teams)':
        ('teams.svg', 'Teams'),
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>(?:Power BI|PowerBI))':
        ('powerbi.svg', 'Power BI'),
    r'<svg[^>]*>.*?</svg>(?=\s*</div>\s*<span[^>]*>VS Code)':
        ('vscode.svg', 'VS Code'),
}

def img_tag(local_file, alt):
    return f'<img src="logos/{local_file}" alt="{alt}" style="width:100%;height:100%;object-fit:contain;">'

total = 0
for filename in sorted(HTML_FILES):
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    count = 0
    for pattern, (local_file, alt) in IMG_REPLACEMENTS.items():
        new_html, n = re.subn(pattern, img_tag(local_file, alt), html, flags=re.DOTALL)
        if n:
            html = new_html
            count += n
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {filename}: {count} SVG→img replacement(s)")
        total += count
    # else:
    #     print(f"   {filename}: no SVG replacements needed")

print(f"\nSVG→img: {total} replacement(s) done.")
