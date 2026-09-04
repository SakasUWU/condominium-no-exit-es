# menu_main: "Rio's phone" -> "Teléfono de Rio"
from PIL import Image, ImageDraw, ImageFont
from imgtools import load, save, F_PIXEL

COL = (205, 201, 196, 255)

if not F_PIXEL:
    raise SystemExit('Falta la fuente VCR OSD Mono; se omite el rótulo del teléfono.')

im = load('pictures', 'menu_main')
px = im.load()
# el fondo es uniforme en horizontal dentro de la pantalla del teléfono
BASE = (9, 9, 9, 255)
for y in range(128, 200):
    ref = px[1021, y]                       # color de la banda justo antes del texto
    for x in range(1022, 1124):
        px[x, y] = ref
    for x in range(1124, 1152):             # se apaga suavemente hacia el borde
        t = (x - 1124) / 27.0
        px[x, y] = tuple(int(ref[i] * (1 - t) + BASE[i] * t) for i in range(4))

d = ImageDraw.Draw(im)
f = ImageFont.truetype(F_PIXEL, 20)
d.text((1028, 136), 'Teléfono', font=f, fill=COL, anchor='lt')
d.text((1028, 164), 'de Rio', font=f, fill=COL, anchor='lt')
save(im, 'pictures', 'menu_main')
print('menu_main -> Teléfono de Rio')
