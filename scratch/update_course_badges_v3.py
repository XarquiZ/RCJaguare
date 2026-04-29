import os

new_badges_html = '''                    <div class="trust-badges" style="margin-bottom: 32px; position: relative; flex-direction: row; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
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
    
    # Pattern to match the trust-badges block from the previous version
    import re
    # The previous block had <div class="trust-badges" ...> ... </div>\n                    </div>
    # and it contained trust-badges-row and floating-benefits-seal
    
    pattern = r'<div class="trust-badges".*?</div>\s*</div>'
    
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, new_badges_html, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename} (compact)")
    else:
        print(f"Could not find trust-badges in {filename}")
