import glob
import re

course_files = glob.glob('/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos/*.html')

for filepath in course_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update title
    title_match = re.search(r'<title>(.*?) \| Rede Comunitá Jaguaré</title>', content)
    if title_match:
        course_name = title_match.group(1)
        new_title = f'<title>Curso de {course_name} Gratuito | Jaguaré, Lapa e Osasco</title>'
        content = re.sub(r'<title>.*?</title>', new_title, content)
    
    # 2. Update description
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    if desc_match:
        original_desc = desc_match.group(1)
        clean_desc = original_desc
        if 'profissionalizante' not in clean_desc.lower():
            if 'Curso gratuito de' in clean_desc:
                clean_desc = clean_desc.replace('Curso gratuito de', 'Curso profissionalizante gratuito de')
            else:
                clean_desc = clean_desc + " Curso profissionalizante gratuito."
                
        new_desc_content = clean_desc + " Certificação SENAI no Jaguaré, com fácil acesso para Lapa e Osasco."
        content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{new_desc_content}">', content)
        
    # 3. Update footer
    footer_old = r'<p>Transformando vidas na região do Jaguaré\.?</p>'
    footer_new = r'<p>Localizados no coração do Jaguaré, recebemos alunos de toda a Zona Oeste de São Paulo, incluindo Lapa, Osasco e arredores. Transformando vidas e construindo um futuro com mais dignidade através de capacitação profissional.</p>'
    content = re.sub(footer_old, footer_new, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Course pages updated.")
