import os
import glob

def update_favicon_tags():
    directory = '/Users/wellintonbatista/Documents/projetos/RCJaguare'
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(directory, '*.html')) + glob.glob(os.path.join(directory, 'cursos', '*.html'))
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Replace occurrences
        content = content.replace('<link rel="shortcut icon" href="images/favicon.png" type="image/png">',
                                  '<link rel="icon" href="images/favicon.png" type="image/png" sizes="192x192">')
                                  
        content = content.replace('<link rel="shortcut icon" href="../images/favicon.png" type="image/png">',
                                  '<link rel="icon" href="../images/favicon.png" type="image/png" sizes="192x192">')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated favicon tags in {filepath}")

if __name__ == "__main__":
    update_favicon_tags()
