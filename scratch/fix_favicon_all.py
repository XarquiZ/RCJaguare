import os
import re

FAVICON_TAGS = """
    <!-- Favicon (Otimizado para o Google Search) -->
    <link rel="icon" href="https://www.cedespjaguare.com.br/images/favicon.png" type="image/png" sizes="192x192">
    <link rel="apple-touch-icon" href="https://www.cedespjaguare.com.br/images/favicon.png">"""

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Se já foi otimizado, remover a versão anterior para evitar duplicação em execuções múltiplas
    if '<!-- Favicon (Otimizado para o Google Search) -->' in content:
        # Remover bloco antigo (uma forma simples é usar expressão regular para remover a seção que inserimos)
        content = re.sub(r'\s*<!-- Favicon \(Otimizado para o Google Search\) -->\s*<link rel="icon"[^>]+>\s*<link rel="apple-touch-icon"[^>]+>', '', content)

    # Passo 1: Remover tags de favicon antigas
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'rel="icon"' in line.lower() or 'rel="shortcut icon"' in line.lower():
            # Não adicionamos as linhas com as tags velhas
            continue
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # Passo 2: Inserir a nova tag logo abaixo do </title>
    match = re.search(r'(</title>)', content, re.IGNORECASE)
    if match:
        insertion_index = match.end()
        new_content = content[:insertion_index] + FAVICON_TAGS + content[insertion_index:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == '__main__':
    directory = '/Users/wellintonbatista/Documents/projetos/RCJaguare'
    html_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    for filepath in html_files:
        if fix_html_file(filepath):
            print(f"Atualizado: {filepath}")
        else:
            print(f"Aviso: <title> não encontrado em {filepath}")
