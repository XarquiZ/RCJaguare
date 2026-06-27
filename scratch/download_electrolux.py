import urllib.request
import os

url = 'https://upload.wikimedia.org/wikipedia/commons/4/42/Electrolux_2015.svg'
dest = '/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos/logos/electrolux.svg'

try:
    print(f"Downloading {url} to {dest}...")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response:
        with open(dest, 'wb') as out_file:
            out_file.write(response.read())
    print("Successfully downloaded Electrolux SVG!")
except Exception as e:
    print("Failed to download:", e)
