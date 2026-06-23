import os
import glob
import re

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file is in a subdirectory (cursos/)
    is_subdir = 'cursos' in filepath
    prefix = '../' if is_subdir else ''
    
    # We want to replace the whole nav-links block to ensure consistency.
    # We'll use regex to find the block and replace it.
    
    pattern = r'<div class="nav-links">.*?</div>'
    
    new_links = f'''<div class="nav-links">
                <a href="{prefix}feira-profissoes.html" class="nav-link-hot-blue">Feira de Profissões</a>
                <a href="{prefix}historia.html">Nossa História</a>
                <a href="{prefix}cursos.html" class="nav-link-animated">Cursos</a>
                <a href="{prefix}eventos.html">Eventos</a>
                <a href="{prefix}calendario.html">Calendário</a>
            </div>'''
            
    # Also handle the active state if it's the current page
    basename = os.path.basename(filepath)
    if basename == 'historia.html':
        new_links = new_links.replace(f'href="{prefix}historia.html"', f'href="{prefix}historia.html" class="active"')
    elif basename == 'cursos.html' or is_subdir:
        new_links = new_links.replace(f'href="{prefix}cursos.html" class="nav-link-animated"', f'href="{prefix}cursos.html" class="nav-link-animated active"')
    elif basename == 'eventos.html':
        new_links = new_links.replace(f'href="{prefix}eventos.html"', f'href="{prefix}eventos.html" class="active"')
    elif basename == 'calendario.html':
        new_links = new_links.replace(f'href="{prefix}calendario.html"', f'href="{prefix}calendario.html" class="active"')
    elif basename == 'feira-profissoes.html':
         new_links = new_links.replace(f'href="{prefix}feira-profissoes.html" class="nav-link-hot-blue"', f'href="{prefix}feira-profissoes.html" class="nav-link-hot-blue active"')
        
    content = re.sub(pattern, new_links, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    base_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare'
    
    files = glob.glob(f'{base_dir}/*.html') + glob.glob(f'{base_dir}/cursos/*.html')
    for f in files:
        replace_in_file(f)
    print("Done applying Feira de Profissoes nav links globally.")
