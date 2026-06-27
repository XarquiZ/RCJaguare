import urllib.request
import re

url = 'https://commons.wikimedia.org/wiki/File:Electrolux_2015.svg'
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Look for hrefs containing upload.wikimedia.org/wikipedia/commons/ and ending with Electrolux_2015.svg
    matches = re.findall(r'https://upload.wikimedia.org/wikipedia/commons/[a-zA-Z0-9_/.-]+/Electrolux_2015.svg', html)
    if matches:
        print("Found URLs:")
        for m in set(matches):
            print(m)
    else:
        print("No matches found.")
except Exception as e:
    print("Error:", e)
