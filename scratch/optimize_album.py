import os
import subprocess
import sys

def install_pillow():
    print("Verificando dependência Pillow (manipulação de imagem)...")
    try:
        from PIL import Image
    except ImportError:
        print("Instalando Pillow automaticamente...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--quiet"])

install_pillow()
from PIL import Image, ImageOps

input_dir = "images/fotos/Halloween 2025"
output_dir = "images/otimizadas/halloween-2025"

os.makedirs(f"{output_dir}/thumb", exist_ok=True)
os.makedirs(f"{output_dir}/full", exist_ok=True)

files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
files.sort()
total = len(files)
print(f"Iniciando conversão WebP de {total} fotos...")

for idx, f in enumerate(files):
    in_path = os.path.join(input_dir, f)
    # Simplify filename to be web friendly, ex: IMG_0643 -> img_0643
    filename = os.path.splitext(f)[0].lower()
    out_thumb = os.path.join(output_dir, "thumb", f"{filename}.webp")
    out_full = os.path.join(output_dir, "full", f"{filename}.webp")
    
    if os.path.exists(out_thumb) and os.path.exists(out_full):
        continue
        
    try:
        with Image.open(in_path) as img:
            # Fix Orientation from EXIF data so portraits don't appear sideways
            img = ImageOps.exif_transpose(img)
            
            rgb_im = img.convert('RGB')
            
            # Save Full
            full_im = rgb_im.copy()
            full_im.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            full_im.save(out_full, 'webp', quality=80)
            
            # Save Thumb
            thumb_im = rgb_im.copy()
            thumb_im.thumbnail((400, 400), Image.Resampling.LANCZOS)
            thumb_im.save(out_thumb, 'webp', quality=75)
            
        print(f"[{idx+1}/{total}] Otimizada: {filename}.webp")
    except Exception as e:
        print(f"Erro em {f}: {str(e)}")

print("🎉 Lote de 97 fotos otimizado com sucesso para WebP!")
