import os

new_badges_html = '''                    <div class="trust-badges" style="margin-bottom: 32px; position: relative;">
                        <!-- Selo Flutuante de Benefícios -->
                        <div class="floating-benefits-seal" style="right: 10%;">
                            <div class="seal-icons">🍴 📚</div>
                            <div class="seal-text">Lanche +<br>Material<br>GRÁTIS</div>
                        </div>

                        <div class="trust-badges-row">
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
                        </div>
                    </div>'''

course_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos'
files = [f for f in os.listdir(course_dir) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(course_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the trust-badges block I created in the previous turn
    if '<div class="trust-badges"' in content:
        # Find the end of this block
        start_index = content.find('<div class="trust-badges"')
        # It's the whole block I added
        # I'll look for the closing </div> of the trust-badges div
        # In the previous script it was:
        # <div class="trust-badges" ...>
        #   <div class="trust-badges-row">...</div>
        #   <div class="free-badge-v2">...</div>
        # </div>
        # That's 4 closing divs: trust-badges-row, senai-badge, bu-badge, free-badge-v2 (plus children)
        # Actually, let's just find the corresponding closing div for the first one.
        
        # Simpler: replace from <div class="trust-badges" to the next </div>\n                    </div>
        # Actually, I'll just use a pattern match for the whole block.
        
        import re
        content = re.sub(r'<div class="trust-badges".*?</div>\s*</div>', new_badges_html, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"Could not find trust-badges in {filename}")
