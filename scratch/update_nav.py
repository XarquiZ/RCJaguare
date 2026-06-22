import os
import glob

def update_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to insert the Jogos de Férias link right after <div class="nav-links">
    
    # Check if already added
    if "jogos-ferias.html" in content or "Jogos de Férias" in content:
        return
        
    # Determine the correct relative path to jogos-ferias.html
    # if the file is in a subdirectory like cursos/, the link should be ../jogos-ferias.html
    rel_prefix = "../" if "cursos/" in filepath else ""
    
    # The new link HTML
    new_link = f'\n                <a href="{rel_prefix}jogos-ferias.html" class="nav-link-hot"><span class="hot-dot"></span> Jogos de Férias</a>'
    
    # We will find <div class="nav-links"> and insert it after.
    # Note: in some files it is <div class="nav-links"><a href...
    
    if '<div class="nav-links">' in content:
        parts = content.split('<div class="nav-links">', 1)
        # Reconstruct
        new_content = parts[0] + '<div class="nav-links">' + new_link + parts[1]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"Warning: nav-links not found in {filepath}")

html_files = glob.glob('*.html') + glob.glob('cursos/*.html')
for file in html_files:
    update_nav(file)
