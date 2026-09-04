// Aplica translation/es.json a los .json de datos del juego y deja el
// resultado en build/www/data/.
//
//   node tools/apply-text.js [--game=...]
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { ROOT, gamePath } = require('./config');
const { extract, apply } = require('./units');

const GAME = gamePath();
const DATA = path.join(GAME, 'www', 'data');
const OUT = path.join(ROOT, 'build', 'www', 'data');

const key = (lines) => crypto.createHash('sha1').update(lines.join('\n'), 'utf8').digest('hex').slice(0, 16);

const es = JSON.parse(fs.readFileSync(path.join(ROOT, 'translation', 'es.json'), 'utf8'));
const units = extract(DATA);

const tr = {};
let hit = 0;
const missing = [];
for (const u of units) {
  const v = es[key(u.lines)];
  if (v) { tr[u.id] = v; hit++; } else missing.push(u);
}

const stats = apply(DATA, OUT, units, tr);
console.log(`texto: ${hit}/${units.length} unidades traducidas -> ${stats.files} archivos en build/www/data`);
if (missing.length) {
  console.log(`sin traducción: ${missing.length} (probablemente el juego ha cambiado de versión)`);
  missing.slice(0, 5).forEach((u) => console.log('   ', u.file, JSON.stringify(u.lines.join(' | ')).slice(0, 90)));
}

// index.html y plugins.js
const js = path.join(GAME, 'www', 'js', 'plugins.js');
let p = fs.readFileSync(js, 'utf8');
const REP = [
  ['"Text Speed 1":"Very Slow"', '"Text Speed 1":"Muy lenta"'],
  ['"Text Speed 2":"Slow"', '"Text Speed 2":"Lenta"'],
  ['"Text Speed 4":"Fast"', '"Text Speed 4":"Rápida"'],
  ['"Text Speed 5":"Faster"', '"Text Speed 5":"Más rápida"'],
  ['"Text Speed 6":"Very Fast"', '"Text Speed 6":"Muy rápida"'],
  ['"Text Speed 7":"Instant"', '"Text Speed 7":"Instantánea"'],
  // los comandos del título son más anchos en español: se corre el centro
  // para que el borde izquierdo del menú no se mueva
  ['"Command Pos 1":"162, 385"', '"Command Pos 1":"222, 385"'],
  ['"Command Pos 2":"164, 435"', '"Command Pos 2":"224, 435"'],
  ['"Command Pos 3":"162,485"', '"Command Pos 3":"222,485"'],
  ['"Command Pos 4":"162,530"', '"Command Pos 4":"222,530"'],
];
let np = 0;
for (const [a, b] of REP) if (p.includes(a)) { p = p.split(a).join(b); np++; }
fs.mkdirSync(path.join(ROOT, 'build', 'www', 'js'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'build', 'www', 'js', 'plugins.js'), p, 'utf8');

let h = fs.readFileSync(path.join(GAME, 'www', 'index.html'), 'utf8');
h = h.replace('CONDOMINIUM: NO EXIT_english', 'CONDOMINIUM: NO EXIT_español');
fs.writeFileSync(path.join(ROOT, 'build', 'www', 'index.html'), h, 'utf8');
console.log(`plugins.js: ${np} ajustes  |  index.html: título de ventana`);
