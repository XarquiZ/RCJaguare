import os
import re

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Sub path based on depth
            eventos_link = "eventos.html"
            if "cursos/" in path:
                eventos_link = "../eventos.html"
                
            new_content = re.sub(
                r'<a href="[^"]*#eventos">Eventos</a>', 
                f'<a href="{eventos_link}">Eventos</a>', 
                content
            )
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {path}")
