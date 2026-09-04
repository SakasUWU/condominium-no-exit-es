// Localiza la carpeta del juego. Orden: argumento --game, variable CONDOMINIUM_PATH,
// config.json en la raíz del repositorio.
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

function gamePath() {
  const arg = process.argv.find((a) => a.startsWith('--game='));
  let p = arg ? arg.slice(7) : process.env.CONDOMINIUM_PATH;
  if (!p) {
    const cfg = path.join(ROOT, 'config.json');
    if (fs.existsSync(cfg)) p = JSON.parse(fs.readFileSync(cfg, 'utf8')).gamePath;
  }
  if (!p) {
    console.error('No se ha indicado la carpeta del juego.\n' +
      'Copia config.example.json a config.json y pon ahí la ruta,\n' +
      'o ejecuta con --game="C:/ruta/a/condominium-demo-win-en".');
    process.exit(1);
  }
  p = p.replace(/\\/g, '/').replace(/\/+$/, '');
  if (!fs.existsSync(path.join(p, 'www', 'data', 'System.json'))) {
    console.error('No parece la carpeta del juego (falta www/data/System.json):', p);
    process.exit(1);
  }
  return p;
}

function encryptionKey(game) {
  const sys = JSON.parse(fs.readFileSync(path.join(game, 'www', 'data', 'System.json'), 'utf8'));
  return sys.encryptionKey;
}

module.exports = { ROOT, gamePath, encryptionKey };
