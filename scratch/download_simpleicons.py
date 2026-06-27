import urllib.request
import os

icons = {
    'electrolux.svg': 'https://unpkg.com/simple-icons@v9/icons/electrolux.svg',
    'alexa.svg': 'https://unpkg.com/simple-icons@v9/icons/amazonalexa.svg',
    'zigbee.svg': 'https://unpkg.com/simple-icons@v9/icons/zigbee.svg'
}

dest_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos/logos'

for filename, url in icons.items():
    dest_path = os.path.join(dest_dir, filename)
    try:
        print(f"Downloading {url} to {dest_path}...")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            with open(dest_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename} from {url}: {e}")
        # Let's write custom high-quality fallback SVGs for the ones that fail
        if 'electrolux' in filename:
            # Simple representation of Electrolux logo or wordmark
            svg = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="45" fill="#011E41"/>
              <path d="M35 30 H65 V40 H47 V47 H60 V57 H47 V64 H65 V74 H35 Z" fill="white"/>
            </svg>'''
        elif 'alexa' in filename:
            svg = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="45" fill="#31C4F3"/>
              <path d="M50 20 C30 20 20 32 20 48 C20 58 26 66 35 71 L35 83 L46 76 C47 76 49 76 50 76 C70 76 80 64 80 48 C80 32 70 20 50 20 Z" fill="white"/>
            </svg>'''
        else:
            svg = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="45" fill="#E60028"/>
              <text x="50" y="58" font-family="sans-serif" font-weight="bold" font-size="24" fill="white" text-anchor="middle">Z</text>
            </svg>'''
        with open(dest_path, 'w') as f:
            f.write(svg)
        print(f"Created high-quality fallback SVG for {filename}")
