# Utilidades para traducir las imagenes del juego
import os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEC = os.path.join(ROOT, 'work', 'img_dec')
OUT = os.path.join(ROOT, 'work', 'img_es')


def _game_path():
    """Ruta del juego: variable de entorno o config.json en la raíz."""
    p = os.environ.get('CONDOMINIUM_PATH')
    if not p:
        cfg = os.path.join(ROOT, 'config.json')
        if os.path.exists(cfg):
            with open(cfg, encoding='utf-8') as fh:
                p = json.load(fh).get('gamePath')
    if not p:
        raise SystemExit('Falta la ruta del juego: crea config.json o define CONDOMINIUM_PATH.')
    return p.replace(os.sep, '/').rstrip('/')


def _find_font(*candidates):
    for c in candidates:
        if c and os.path.exists(c):
            return c
    raise SystemExit('No se encuentra ninguna de estas fuentes: ' + ', '.join(str(c) for c in candidates))


_WINF = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
_USERF = os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts')

# Fuente del propio juego (Paperlogy): se toma de la copia del usuario.
F_GAME = os.path.join(_game_path(), 'www/fonts/Paperlogy-4Regular.ttf')
# Fuentes de sistema usadas para recrear los rótulos.
F_DISPLAY = _find_font(os.path.join(_WINF, 'seguibl.ttf'), os.path.join(_WINF, 'ariblk.ttf'))
F_UI = _find_font(os.path.join(_WINF, 'Roboto-Regular.ttf'), os.path.join(_WINF, 'segoeui.ttf'))
F_UI_B = _find_font(os.path.join(_WINF, 'segoeuib.ttf'), os.path.join(_WINF, 'arialbd.ttf'))
# Fuente de píxeles para el rótulo del teléfono (opcional).
F_PIXEL = None
for _c in (os.path.join(_USERF, 'VCR_OSD_MONO_1.001.ttf'), os.path.join(_WINF, 'VCR_OSD_MONO_1.001.ttf')):
    if os.path.exists(_c):
        F_PIXEL = _c
        break

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def load(sub, name):
    return Image.open(os.path.join(DEC, sub, name + '.png')).convert('RGBA')

def load_es(sub, name):
    """Carga la version ya traducida si existe; si no, el original."""
    p = os.path.join(OUT, sub, name + '.png')
    if os.path.exists(p):
        return Image.open(p).convert('RGBA')
    return load(sub, name)


def save(im, sub, name):
    d = os.path.join(OUT, sub)
    os.makedirs(d, exist_ok=True)
    im.save(os.path.join(d, name + '.png'))
    return os.path.join(d, name + '.png')

def clear(im, box):
    """Deja transparente un rectangulo (x0,y0,x1,y1)."""
    im.paste((0, 0, 0, 0), box)

def fill(im, box, color):
    im.paste(color, box)

def text_w(txt, f):
    return f.getbbox(txt)[2] - f.getbbox(txt)[0]

def draw_text(im, xy, txt, f, fill_color, outline=None, ow=0, shadow=None, soff=(2, 2), sblur=0,
              anchor='la', condense=1.0):
    """Dibuja texto con contorno y sombra opcionales. condense<1 aprieta horizontalmente."""
    if condense != 1.0:
        # renderiza en una capa aparte y la escala horizontalmente
        pad = 40
        bb = f.getbbox(txt)
        w = bb[2] - bb[0] + 2 * pad + 2 * ow
        h = bb[3] - bb[1] + 2 * pad + 2 * ow
        lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        _draw_one(lay, (pad - bb[0] + ow, pad - bb[1] + ow), txt, f, fill_color, outline, ow, shadow, soff, sblur, 'la')
        lay = lay.resize((max(1, int(w * condense)), h), Image.LANCZOS)
        padc = pad * condense
        ink_w = lay.width - 2 * padc
        x, y = xy
        if anchor[0] == 'm':
            x -= ink_w / 2
        elif anchor[0] == 'r':
            x -= ink_w
        im.alpha_composite(lay, (int(round(x - padc)), int(y - pad)))
        return
    _draw_one(im, xy, txt, f, fill_color, outline, ow, shadow, soff, sblur, anchor)

def _draw_one(im, xy, txt, f, fill_color, outline, ow, shadow, soff, sblur, anchor):
    if shadow:
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.text((xy[0] + soff[0], xy[1] + soff[1]), txt, font=f, fill=shadow, anchor=anchor,
               stroke_width=ow, stroke_fill=shadow)
        if sblur:
            lay = lay.filter(ImageFilter.GaussianBlur(sblur))
        im.alpha_composite(lay)
    d = ImageDraw.Draw(im)
    if outline and ow:
        d.text(xy, txt, font=f, fill=fill_color, anchor=anchor, stroke_width=ow, stroke_fill=outline)
    else:
        d.text(xy, txt, font=f, fill=fill_color, anchor=anchor)

def fit_font(path, txt, max_w, start, min_size=8):
    """Mayor tamaño de fuente cuyo texto cabe en max_w."""
    s = start
    while s > min_size and text_w(txt, font(path, s)) > max_w:
        s -= 1
    return font(path, s)

def sample(im, x, y):
    return im.getpixel((x, y))
