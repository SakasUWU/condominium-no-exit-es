# Avisos de esquina: "Objective Updated!" / "Gallery Updated!"
from PIL import Image
from imgtools import load, save, font, draw_text, F_DISPLAY

RED = (180, 5, 0, 255)
BLACK = (13, 14, 14, 255)

for name, txt in [('guide0', '¡Objetivo actualizado!'), ('guide0_0', '¡Galería actualizada!')]:
    src = load('pictures', name)
    im = Image.new('RGBA', src.size, (0, 0, 0, 0))
    draw_text(im, (15, 676), txt, font(F_DISPLAY, 31), RED,
              outline=BLACK, ow=3, condense=0.82, anchor='la')
    save(im, 'pictures', name)
    print(name, txt)
