# CONDOMINIUM: NO EXIT — traducción al español

Traducción completa al **español neutro latinoamericano** de la demo de
*CONDOMINIUM: NO EXIT*, el juego de terror en RPG Maker MV de HWADON.

Traducción no oficial hecha por fans. No está afiliada al equipo del juego.

---

## Qué incluye

| | |
|---|---|
| **Texto** | 1555 unidades: diálogos, narración, opciones, objetos, descripciones y términos del motor |
| **Imágenes** | 67 archivos con texto incrustado, rehechos respetando fuente, color y posición |
| **Extra** | Los fragmentos que la versión inglesa había dejado en **coreano** (varios objetos, notas y mensajes del sistema) también están traducidos |

Imágenes traducidas: menú del título, menú del teléfono (Objetos, Galería,
Mensajes, Guardar, Opciones, Salir), las siete pantallas de GUÍA, los fondos
de las pantallas de menú, el mensajero completo (objetivos, conversación con
Jun, los mensajes distorsionados y el aviso de la estación), los consejos de
la pantalla de muerte, el aviso de contenido, "Sin servicio", las barras de
sistema, los créditos y la pantalla de fin de demo.

## Criterios de traducción

- **Por sentido, no literal.** Se prioriza el tono, el subtexto y el ritmo
  del original por encima de la correspondencia palabra por palabra.
- **Códigos de control intactos.** `\c[n]`, `\i[n]`, `\.`, `\|`, `\^`,
  `\{ \}`, `\TA[n]` y `\Shake<>` se conservan exactamente, igual que la
  sangría con espacios ideográficos que el juego usa para los diálogos.
- **Sin desbordes.** Cada línea se mide con la fuente real del juego
  (Paperlogy) para comprobar que cabe en el cuadro de mensaje.
- **Nombres propios** (RIO, Jun) y el título del juego se mantienen.

---

## Cómo usarlo

Necesitas tu propia copia de la demo. Este repositorio **no contiene ningún
archivo del juego**: solo las traducciones y las herramientas que generan el
parche a partir de tu copia.

### 1. Requisitos

- [Node.js](https://nodejs.org) 18 o superior
- [Python](https://www.python.org) 3.9 o superior con `pillow` y `numpy`
  (solo para las imágenes): `pip install pillow numpy`
- Windows, por las fuentes del sistema que se usan al recrear los rótulos

### 2. Configuración

```bash
git clone https://github.com/SakasUWU/condominium-no-exit-es
cd condominium-no-exit-es
cp config.example.json config.json
```

Edita `config.json` y pon la ruta de tu copia del juego (la carpeta que
contiene `Game.exe`):

```json
{ "gamePath": "C:/ruta/a/condominium-demo-win-en" }
```

### 3. Generar el parche

```bash
node build.js
```

Queda en `build/`. Copia su contenido sobre la carpeta del juego y acepta
reemplazar. Haz antes una copia de `www/data`, `www/img`, `www/js/plugins.js`
e `www/index.html` si quieres poder volver al inglés.

Si solo quieres el texto y no las imágenes: `node build.js --skip-images`

---

## Cómo funciona

```
translation/es.json   traducciones indexadas por hash del texto original
tools/units.js        extrae/reinyecta las unidades de traducción de los .json
tools/apply-text.js   aplica el texto y ajusta plugins.js e index.html
tools/rpgmv-crypt.js  cifrado/descifrado de recursos .rpgmvp de RPG Maker MV
tools/images.js       descifra las imágenes y vuelve a cifrar las traducidas
tools/img_*.py        recrean cada grupo de imágenes con texto en español
tools/textwidth.js    mide texto con las métricas reales del TTF del juego
build.js              orquesta todo el proceso
```

Las traducciones **no se indexan por posición** sino por el hash SHA-1 del
texto original de cada bloque. Eso tiene dos ventajas: el parche sigue
funcionando aunque cambien los ids internos del juego, y el repositorio no
guarda ni una línea del texto del autor.

Las unidades de traducción respetan los bloques de mensaje completos (no
líneas sueltas), de modo que el reparto entre líneas se puede rehacer en
español sin romper el ritmo del diálogo.

Para las imágenes, cuando el texto original tapaba el fondo se reconstruye
antes de reescribir: la plancha limpia del panel de GUÍA y de los rótulos del
teléfono se obtiene combinando las variantes de cada imagen y quedándose con
el píxel más oscuro, que elimina el texto y deja el fondo intacto.

---

## Estado

Traducido y probado sobre la build de la demo del 28 de agosto de 2026.
Si sale una versión nueva, las líneas cuyo texto original no haya cambiado se
siguen aplicando solas; `node build.js` avisa de las que queden sin traducir.

## Créditos

- Traducción y herramientas: **SakasUWU**
- Juego original: **HWADON** — [CONDOMINIUM: NO EXIT en Steam](https://store.steampowered.com/app/4255130/CONDOMINIUM_NO_EXIT)

Si te gusta el juego, añádelo a tu lista de deseos y apoya a sus autores.
