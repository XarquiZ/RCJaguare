import os
import re

# We want the clean compact badges structure
clean_badges_html = '''                    <div class="trust-badges" style="margin-bottom: 32px; position: relative; flex-direction: row; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                        <div class="trust-badge senai-badge">
                            <div class="badge-logo-container">
                                <img src="../images/logo_senai.png?v=1.2" alt="SENAI">
                            </div>
                            <div class="badge-text">
                                <span class="badge-title">Certificação Oficial</span>
                                <span class="badge-sub">Padrão SENAI</span>
                            </div>
                        </div>
                        <div class="trust-badge bu-badge">
                            <div class="badge-logo-container">
                                <img src="../images/logobu.png" alt="Bilhete Único">
                            </div>
                            <div class="badge-text">
                                <span class="badge-title">Bilhete Único</span>
                                <span class="badge-sub">Passe Livre Estudantil</span>
                            </div>
                        </div>

                        <!-- Selo Flutuante de Benefícios -->
                        <div class="floating-benefits-seal" style="top: -20px; right: -10px;">
                            <div class="seal-icons">🍴 📚</div>
                            <div class="seal-text">Lanche +<br>Material<br>GRÁTIS</div>
                        </div>
                    </div>'''

course_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos'
files = [f for f in os.listdir(course_dir) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(course_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Identify the whole messy block. 
    # It starts with the first <div class="trust-badges" and ends with the last closing div of the badges section.
    # Looking at the view_file, it's a mess of nested divs.
    
    # Let's find the start of the first trust-badges and the end of the last trust-badges/free-badge-v2 block.
    start_match = re.search(r'<div class="trust-badges".*?>', content)
    if start_match:
        start_idx = start_match.start()
        # Find the last closing tag of the whole badges block.
        # It's usually followed by the h1 course-title.
        end_match = re.search(r'</div>\s*<h1 class="course-title"', content)
        if end_match:
            end_idx = end_match.start() + 6
            content = content[:start_idx] + clean_badges_html + content[end_idx:]
            
            # Also align the course hero content
            # Remove margin-bottom from hero-badges if I added it elsewhere or adjust hero-pills
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned and updated {filename}")
        else:
            print(f"Could not find end for {filename}")
    else:
        print(f"No trust-badges found in {filename}")
