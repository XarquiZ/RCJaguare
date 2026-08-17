import os
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def update_wa_link(match):
    full_url = match.group(0)
    parsed_url = urlparse(full_url)
    query_params = parse_qs(parsed_url.query)
    
    # User requested to use the exact same message for all links:
    # "Olá! Vim pelo site e quero me matricular."
    new_text = "Olá! Vim pelo site e quero me matricular."
        
    query_params['text'] = [new_text]
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
    
    return new_url

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match https://wa.me/... up to the closing quote (but don't include quote in match group, handle quotes outside)
    # The regex will match just the URL
    pattern = r'https://wa\.me/[^\s\"\'\>]+'
    
    new_content = re.sub(pattern, update_wa_link, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")

def main():
    directory = '/Users/wellintonbatista/Documents/projetos/RCJaguare'
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html') or file.endswith('.py'):
                filepath = os.path.join(root, file)
                # Ignore the script itself
                if os.path.basename(filepath) == 'update_whatsapp_message.py':
                    continue
                update_file(filepath)

if __name__ == '__main__':
    main()
