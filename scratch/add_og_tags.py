import glob
import re

# Defina o domínio real aqui para que as imagens funcionem no WhatsApp!
DOMAIN = "https://cedespjaguare.com.br" 
IMAGE_PATH = f"{DOMAIN}/images/logo_rede_comunita.png"

files = glob.glob('/Users/wellintonbatista/Documents/projetos/RCJaguare/*.html') + glob.glob('/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos/*.html')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Se já tiver OG tags, pula para não duplicar
    if 'property="og:title"' in content:
        # Opcional: remover as antigas se precisar rodar de novo
        content = re.sub(r'<!-- Open Graph.*?-->.*?<meta name="twitter:image".*?>', '', content, flags=re.DOTALL)

    # Extrai o título existente
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else 'Rede Comunitá Jaguaré'
    
    # Extrai a descrição existente
    desc_match = re.search(r'<meta name="description"\s+content="(.*?)">', content)
    desc = desc_match.group(1) if desc_match else 'Transformando vidas na região do Jaguaré através da educação.'
    
    og_tags = f'''
    <!-- Open Graph / Redes Sociais -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{IMAGE_PATH}">
    
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{IMAGE_PATH}">
    '''
    
    # Insere antes de fechar o head
    if '</head>' in content:
        content = content.replace('</head>', f'{og_tags}\n</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Tags Open Graph (Cards para WhatsApp) adicionadas em todas as páginas!")
