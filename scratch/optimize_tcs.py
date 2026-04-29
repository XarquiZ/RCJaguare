import os
from PIL import Image, ImageOps

input_dir = "images/fotos/TCS 2025"
output_dir = "images/otimizadas/tcs-2025"

os.makedirs(f"{output_dir}/thumb", exist_ok=True)
os.makedirs(f"{output_dir}/full", exist_ok=True)

files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
files.sort()
total = len(files)
print(f"Iniciando conversão WebP de {total} fotos do TCS 2025...")

for idx, f in enumerate(files):
    in_path = os.path.join(input_dir, f)
    filename = os.path.splitext(f)[0].lower().replace(" ", "_")
    out_thumb = os.path.join(output_dir, "thumb", f"{filename}.webp")
    out_full = os.path.join(output_dir, "full", f"{filename}.webp")
    
    if os.path.exists(out_thumb) and os.path.exists(out_full):
        continue
        
    try:
        with Image.open(in_path) as img:
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

print("🎉 Lote TCS 2025 otimizado com sucesso para WebP!")
