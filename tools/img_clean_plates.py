# Genera la "plancha limpia" del panel de GUÍA.
# Los seis guide*.png comparten fondo y solo cambia el texto, así que
# quedándonos con el píxel más oscuro de los seis desaparece el texto
# y queda el panel vacío.
import os
import numpy as np
from PIL import Image
from imgtools import DEC

NAMES = ['guide1', 'guide2', 'guide3', 'guide4', 'guide5', 'guide6']
src = [os.path.join(DEC, 'pictures', n + '.png') for n in NAMES]
missing = [p for p in src if not os.path.exists(p)]
if missing:
    raise SystemExit('Faltan imágenes descifradas: ' + ', '.join(os.path.basename(m) for m in missing))

st = np.stack([np.array(Image.open(p).convert('RGBA')).astype(np.int32) for p in src])
idx = np.argmin(st[:, :, :, :3].sum(3), axis=0)
out = np.take_along_axis(st, idx[None, :, :, None], axis=0)[0].astype('uint8')
dest = os.path.join(DEC, 'pictures', '_guide_clean.png')
Image.fromarray(out, 'RGBA').save(dest)
print('plancha limpia del panel de GUÍA ->', os.path.basename(dest))
