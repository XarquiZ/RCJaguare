import os
import sys
import subprocess

def install_pillow():
    try:
        from PIL import Image
    except ImportError:
        print("Installing Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

install_pillow()

from PIL import Image

def make_square(im, min_size=192, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    # Paste the original image into the center
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    # Resize to min_size
    return new_im.resize((min_size, min_size), Image.Resampling.LANCZOS)

def process_favicon():
    favicon_path = 'images/favicon.png'
    if not os.path.exists(favicon_path):
        print(f"Error: {favicon_path} not found.")
        return

    img = Image.open(favicon_path).convert("RGBA")
    print(f"Original size: {img.size}")
    
    sq_img = make_square(img, min_size=192)
    sq_img.save(favicon_path)
    print(f"Favicon resized and saved successfully. New size: {sq_img.size}")

if __name__ == "__main__":
    process_favicon()
