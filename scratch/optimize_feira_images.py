import os
from PIL import Image
import glob

# Diretorios
input_dir = 'images/fotos/feira'
output_dir = 'images/otimizadas/feira'

# Criar pasta de saida se nao existir
os.makedirs(output_dir, exist_ok=True)

# Buscar todas as imagens jpg na pasta da feira
image_files = glob.glob(os.path.join(input_dir, '*.jpg'))

for filepath in image_files:
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    # Abrir imagem
    with Image.open(filepath) as img:
        # Converter se não for RGB (por exemplo RGBA)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Otimizar tamanho maximo (Redimensionar mantendo proporção)
        max_size = (1200, 1200)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Salvar como WebP com qualidade 80
        output_path = os.path.join(output_dir, f"{name}.webp")
        img.save(output_path, 'webp', quality=80, optimize=True)
        
        print(f"Otimizado: {filename} -> {name}.webp")

print("Todas as fotos da feira foram otimizadas e convertidas para WebP!")
