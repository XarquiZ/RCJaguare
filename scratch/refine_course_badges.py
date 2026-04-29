import os

course_dir = '/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos'
files = [f for f in os.listdir(course_dir) if f.endswith('.html')]

for filename in files:
    filepath = os.path.join(course_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add a container for eyebrows to handle spacing
    old_block = '''                    <div class="hero-eyebrow">
                        <img class="senai-img" src="../images/logo_senai.png" alt="SENAI">
                        <span>Certificação SENAI Oficial</span>
                    </div>
                    <div class="hero-eyebrow">
                        <img class="senai-img" src="../images/logobu.png" alt="Bilhete Único">
                        <span>Passe Livre Estudantil</span>
                    </div>'''
                    
    new_block = '''                    <div class="hero-badges" style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 28px;">
                        <div class="hero-eyebrow" style="margin-bottom: 0;">
                            <img class="senai-img" src="../images/logo_senai.png" alt="SENAI">
                            <span>Certificação SENAI Oficial</span>
                        </div>
                        <div class="hero-eyebrow" style="margin-bottom: 0;">
                            <img class="senai-img" src="../images/logobu.png" alt="Bilhete Único">
                            <span>Passe Livre Estudantil</span>
                        </div>
                    </div>'''
    
    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Refined {filename}")
    else:
        print(f"Could not find block in {filename}")
