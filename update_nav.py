import os
import glob

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Root files
    content = content.replace('<a href="cursos.html">Cursos</a>', '<a href="cursos.html" class="nav-link-animated">Cursos</a>')
    # Subdir files
    content = content.replace('<a href="../cursos.html">Cursos</a>', '<a href="../cursos.html" class="nav-link-animated">Cursos</a>')
    
    with open(filepath, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    base_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare'
    # HTML files in root
    for f in glob.glob(f'{base_dir}/*.html'):
        replace_in_file(f)
    # HTML files in cursos/
    for f in glob.glob(f'{base_dir}/cursos/*.html'):
        replace_in_file(f)
    print("Done replacing nav links.")
