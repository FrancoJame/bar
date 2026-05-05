from pathlib import Path
from PIL import Image

src = Path('media/products/club.jpg')
dest = Path('products/static/products/icons')
dest.mkdir(parents=True, exist_ok=True)
img = Image.open(src).convert('RGBA')
for size, name in [(192, 'icon-192x192.png'), (512, 'icon-512x512.png'), (192, 'icon-maskable.png')]:
    out = img.resize((size, size), Image.LANCZOS)
    out.save(dest / name, format='PNG')
print('icons generated:', [str(p) for p in dest.iterdir()])
