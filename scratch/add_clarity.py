import os
import glob

CLARITY_SCRIPT = """
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "xcmmujogo7");
    </script>"""

def add_clarity_script():
    directory = '/Users/wellintonbatista/Documents/projetos/RCJaguare'
    
    # Find all HTML files
    html_files = glob.glob(os.path.join(directory, '*.html')) + glob.glob(os.path.join(directory, 'cursos', '*.html'))
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Check if already has Clarity
        if "xcmmujogo7" not in content:
            # Insert before </head>
            content = content.replace('</head>', CLARITY_SCRIPT + '\n</head>')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added Clarity script to {filepath}")

if __name__ == "__main__":
    add_clarity_script()
