# Imágenes sueltas: aviso de contenido, "sin servicio", consejos de muerte,
# menú de game over, barras de sistema y la etiqueta del mensajero.
import numpy as np
from PIL import Image, ImageDraw
from imgtools import load, save, font, draw_text, text_w, F_GAME, F_DISPLAY

RED = (165, 9, 0, 255)
RED2 = (180, 5, 0, 255)
GREY = (222, 222, 222, 255)
LIGHT = (187, 183, 180, 255)
BLACK = (13, 14, 14, 255)
CX = 640


def runs_x(a, y0, y1, th=100):
    m = a[y0:y1, :, 3] > th
    cols = m.sum(0)
    out, s = [], None
    for i, v in enumerate(cols):
        if v > 0 and s is None:
            s = i
        elif v == 0 and s is not None:
            out.append((s, i))
            s = None
    if s is not None:
        out.append((s, len(cols)))
    return out


# ---------------- dannger3: advertencia de contenido ----------------
im = load('pictures', 'dannger3')
d = ImageDraw.Draw(im)
im.paste((0, 0, 0, 0), (300, 296, 980, 505))
LINES = [
    (310, 'Este juego contiene escenas de violencia,', RED, 22),
    (334, 'imágenes perturbadoras, sustos repentinos', RED, 22),
    (358, 'y otro contenido gráfico que puede resultar', RED, 22),
    (382, 'impactante para algunos jugadores.', RED, 22),
    (429, 'Todo lo que aquí se muestra es ficticio', GREY, 22),
    (453, 'y no está basado en, ni relacionado con,', GREY, 22),
    (477, 'hechos o personas reales.', GREY, 22),
]
for y, txt, col, size in LINES:
    d.text((CX, y), txt, font=font(F_GAME, size), fill=col, anchor='ma')
# botón "Warning"
im.paste(RED, (540, 190, 730, 228))
draw_text(im, (634, 192), 'Advertencia', font(F_DISPLAY, 26), (20, 0, 0, 255), condense=0.9, anchor='ma')
save(im, 'pictures', 'dannger3')
print('dannger3 ok')

# ---------------- dannger4: sin servicio ----------------
im = load('pictures', 'dannger4')
d = ImageDraw.Draw(im)
im.paste((8, 8, 8, 255), (915, 388, 1132, 492))
d.text((1023, 392), 'Sin servicio', font=font(F_GAME, 26), fill=(166, 12, 0, 255), anchor='ma')
d.text((1023, 428), 'Buscando', font=font(F_GAME, 20), fill=LIGHT, anchor='ma')
d.text((1023, 452), 'señal…', font=font(F_GAME, 20), fill=LIGHT, anchor='ma')
save(im, 'pictures', 'dannger4')
print('dannger4 ok')

# ---------------- consejos de la pantalla de muerte ----------------
TIPS = {
    'deadmenu10': ['¿Te deshiciste de todo lo innecesario?'],
    'deadmenu11': ['¿Qué objeto podría demostrar quién eres?'],
    'deadmenu12': ['Los residentes corren más que tú.'],
    'deadmenu2': ['Lleva siempre un guardián', 'cuando te adentres en la oscuridad.'],
    'deadmenu7': ['El cuerpo humano es más frágil de lo que crees.'],
    'deadmenu8': ['¡Cuida mejor tu HP!'],
    'deadmenu9': ['¿No se te olvidó algo?'],
}
for name, lines in TIPS.items():
    src = load('pictures', name)
    a = np.array(src)
    band = (630, 695)
    rx = runs_x(a, *band)
    bx0, bx1 = rx[0]                      # la pastilla "TIP"
    badge = src.crop((bx0, band[0], bx1 + 1, band[1]))
    f = font(F_GAME, 24)
    tw = max(text_w(t, f) for t in lines)
    gap = 14
    total = badge.width + gap + tw
    x = CX - total // 2
    im = Image.new('RGBA', src.size, (0, 0, 0, 0))
    im.alpha_composite(badge, (x, band[0]))
    d = ImageDraw.Draw(im)
    if len(lines) == 1:
        d.text((x + badge.width + gap, 651), lines[0], font=f, fill=RED2, anchor='lt')
    else:
        for i, t in enumerate(lines):
            d.text((x + badge.width + gap, 639 + i * 26), t, font=f, fill=RED2, anchor='lt')
    save(im, 'pictures', name)
print('consejos ok')

# ---------------- menú de game over ----------------
for name, txt, cx in [('deadmenu3', 'Llamada', 439), ('deadmenu4', 'Salir', 843)]:
    im = load('pictures', name)
    im.paste((6, 6, 6, 255), (cx - 155, 556, cx + 155, 594))
    ImageDraw.Draw(im).text((cx, 558), txt, font=font(F_GAME, 28), fill=(222, 222, 222, 255), anchor='ma')
    save(im, 'pictures', name)
for name, txt, cx in [('deadmenu5', 'Llamada', 438), ('deadmenu6', 'Salir', 841)]:
    src = load('pictures', name)
    a = np.array(src)
    im = src.copy()
    im.paste((0, 0, 0, 0), (cx - 130, 540, cx + 130, 600))
    draw_text(im, (cx, 548), txt, font(F_DISPLAY, 28), RED2, outline=BLACK, ow=3,
              condense=0.88, anchor='ma')
    save(im, 'pictures', name)
print('game over ok')

# ---------------- barras de sistema ----------------
for name, txt in [('system_bar1', '¡Ahora!'), ('system_bar2', 'Pulsa Z')]:
    src = load('pictures', name)
    a = np.array(src)
    im = src.copy()
    # el degradado es uniforme en horizontal: se reconstruye fila a fila
    px = im.load()
    for y in range(566, 626):
        col = px[1000, y]
        for x in range(352, 600):
            px[x, y] = col
    f = font(F_DISPLAY, 21)
    draw_text(im, (354, 582), txt, f, RED2, outline=BLACK, ow=3, condense=0.88, anchor='la')
    save(im, 'pictures', name)
    print(name, 'ok')

# ---------------- etiqueta del mensajero ----------------
im = load('pictures', 'message_icon1')
im.paste((165, 10, 0, 255), (228, 146, 317, 176))
ImageDraw.Draw(im).text((273, 152), 'Cadena', font=font(F_GAME, 17), fill=(26, 26, 26, 255), anchor='ma')
save(im, 'pictures', 'message_icon1')
print('message_icon1 ok')
