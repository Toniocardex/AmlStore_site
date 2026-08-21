import os
from PIL import Image

SRC = r'C:\Users\Anton\.cursor\projects\c-Users-Anton-Desktop-AmlStore-site\assets\c__Users_Anton_AppData_Roaming_Cursor_User_workspaceStorage_9033966f7805af44416d15a720174b72_images_media_asset_Security-52d268ab-d0d0-4beb-b3c3-0de7dea02d17.png'
OUT = r'asset\media\security-protection-bg.webp'

src = Image.open(SRC).convert('RGB')
w, h = src.size
keyed = Image.new('RGBA', (w, h))
sp, kp = src.load(), keyed.load()

# Lo sfondo nero dell'asset diventa alpha: il canale piu' luminoso fa da
# maschera e l'RGB viene "un-premultiplied" per evitare la frangia scura.
for y in range(h):
    for x in range(w):
        r, g, b = sp[x, y]
        v = max(r, g, b)
        if v < 4:
            kp[x, y] = (0, 0, 0, 0)
        else:
            a = v / 255.0
            kp[x, y] = (
                min(255, int(r / a)),
                min(255, int(g / a)),
                min(255, int(b / a)),
                min(255, int(v * 1.05)),
            )

# Renderizzata in un box da ~420x550 CSS px: 480x640 copre con margine.
keyed.resize((480, 640), Image.LANCZOS).save(OUT, 'WEBP', quality=78, method=6)
print('written', OUT, os.path.getsize(OUT), 'bytes')
