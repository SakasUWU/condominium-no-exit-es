// Descifra las imágenes del juego a work/img_dec/ (para que los scripts de
// Python las editen) y vuelve a cifrar work/img_es/ en build/www/img/.
//
//   node tools/images.js decrypt [--game=...]
//   node tools/images.js encrypt [--game=...]
const fs = require('fs');
const path = require('path');
const { ROOT, gamePath, encryptionKey } = require('./config');
const { decrypt, encrypt } = require('./rpgmv-crypt');

const GAME = gamePath();
const KEY = encryptionKey(GAME);
const DIRS = ['pictures', 'system', 'titles1', 'titles2'];
const DEC = path.join(ROOT, 'work', 'img_dec');
const ES = path.join(ROOT, 'work', 'img_es');

if (process.argv[2] === 'decrypt') {
  let n = 0;
  for (const d of DIRS) {
    const src = path.join(GAME, 'www', 'img', d);
    if (!fs.existsSync(src)) continue;
    const out = path.join(DEC, d);
    fs.mkdirSync(out, { recursive: true });
    for (const f of fs.readdirSync(src)) {
      if (f.endsWith('.rpgmvp')) {
        fs.writeFileSync(path.join(out, f.replace('.rpgmvp', '.png')), decrypt(fs.readFileSync(path.join(src, f)), KEY));
        n++;
      } else if (f.endsWith('.png')) {
        fs.copyFileSync(path.join(src, f), path.join(out, f));
        n++;
      }
    }
  }
  console.log('descifradas', n, 'imágenes en work/img_dec/');
} else if (process.argv[2] === 'encrypt') {
  if (!fs.existsSync(ES)) { console.error('No existe work/img_es/. Ejecuta antes los scripts de imagen.'); process.exit(1); }
  let n = 0;
  for (const d of fs.readdirSync(ES)) {
    const out = path.join(ROOT, 'build', 'www', 'img', d);
    fs.mkdirSync(out, { recursive: true });
    for (const f of fs.readdirSync(path.join(ES, d))) {
      if (!f.endsWith('.png')) continue;
      fs.writeFileSync(path.join(out, f.replace('.png', '.rpgmvp')), encrypt(fs.readFileSync(path.join(ES, d, f)), KEY));
      n++;
    }
  }
  console.log('cifradas', n, 'imágenes en build/www/img/');
} else {
  console.log('uso: node tools/images.js decrypt|encrypt');
}
