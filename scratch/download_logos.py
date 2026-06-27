import urllib.request
import os

logos = {
    'electrolux.svg': 'https://upload.wikimedia.org/wikipedia/commons/9/9b/Electrolux_2015.svg',
    'alexa.svg': 'https://upload.wikimedia.org/wikipedia/commons/0/0c/Amazon_Alexa_logo.svg',
    'zigbee.svg': 'https://upload.wikimedia.org/wikipedia/commons/d/da/Zigbee_logo.svg'
}

dest_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos/logos'

for filename, url in logos.items():
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
        # Write a fallback SVG if download fails
        with open(dest_path, 'w') as f:
            f.write('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><text x="10" y="50" font-family="sans-serif" font-size="12" fill="black">' + filename.split('.')[0] + '</text></svg>')
