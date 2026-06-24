import os
import glob

GA_SCRIPT = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-HSJD5ZEQTG"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-HSJD5ZEQTG');
    </script>"""

def add_ga_script():
    directory = '/Users/wellintonbatista/Documents/projetos/RCJaguare'
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(directory, '*.html')) + glob.glob(os.path.join(directory, 'cursos', '*.html'))
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Check if already has GA
        if "G-HSJD5ZEQTG" not in content:
            # Insert after <head>
            content = content.replace('<head>', '<head>\n' + GA_SCRIPT)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added GA script to {filepath}")

if __name__ == "__main__":
    add_ga_script()
