import os
import json

base_dir = "images/otimizadas"
albums = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

album_data = {}
total_images = 0

for album_id in albums:
    thumb_dir = os.path.join(base_dir, album_id, "thumb")
    if not os.path.exists(thumb_dir): continue
    
    files = [f for f in os.listdir(thumb_dir) if f.lower().endswith('.webp')]
    files.sort()
    
    # Auto-generate title
    title = album_id.replace('-', ' ').title()
    if "2025" in title:
        title = title.replace("2025", "2025").strip()
        
    album_data[album_id] = {
        "title": f"Fotos de {title}",
        "path": f"{base_dir}/{album_id}/",
        "images": files
    }
    total_images += len(files)

js_content = f"const ALBUMS_DATA = {json.dumps(album_data, indent=4)};"
with open("albums_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Gerado albums_data.js com sucesso! {total_images} imagens encontradas em {len(album_data)} álbuns.")
