import os

badge_html = '''                    <div class="trust-badge bu-badge">
                        <img src="../images/logobu.png" alt="Bilhete Único" class="badge-icon">
                        <div class="badge-text">
                            <span class="badge-title">Bilhete Único</span>
                            <span class="badge-sub">Passe Livre Estudantil</span>
                        </div>
                    </div>'''

course_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos'
files = [f for f in os.listdir(course_dir) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(course_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has bu-badge
    if 'bu-badge' in content:
        continue
        
    # In course pages, the badges are different (hero-eyebrow or hero-pills)
    # Actually, in the last check, I saw hero-eyebrow:
    # <div class="hero-eyebrow">
    #     <img class="senai-img" src="../images/logo_senai.png" alt="SENAI">
    #     <span>Certificação SENAI Oficial</span>
    # </div>
    
    # Let's add it as a second hero-eyebrow or expand the first one.
    # The user wants "mesmo destaque do SENAI".
    
    new_eyebrow = '''                    <div class="hero-eyebrow">
                        <img class="senai-img" src="../images/logo_senai.png" alt="SENAI">
                        <span>Certificação SENAI Oficial</span>
                    </div>
                    <div class="hero-eyebrow">
                        <img class="senai-img" src="../images/logobu.png" alt="Bilhete Único">
                        <span>Passe Livre Estudantil</span>
                    </div>'''
    
    old_eyebrow = '''                    <div class="hero-eyebrow">
                        <img class="senai-img" src="../images/logo_senai.png" alt="SENAI">
                        <span>Certificação SENAI Oficial</span>
                    </div>'''
    
    if old_eyebrow in content:
        content = content.replace(old_eyebrow, new_eyebrow)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"Could not find eyebrow in {filename}")
