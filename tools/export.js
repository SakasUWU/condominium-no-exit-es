// Exporta las traducciones a translation/es.json, indexadas por el hash del
// texto original. Así el parche sigue funcionando aunque cambien los ids
// internos, y el repositorio no guarda ni una línea del texto del autor.
//
//   node tools/export.js <carpeta-work> <salida>
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORK = process.argv[2] || path.join(__dirname, '..', '..', 'CondominiumES', 'work');
const OUT = process.argv[3] || path.join(__dirname, '..', 'translation', 'es.json');

const key = (lines) => crypto.createHash('sha1').update(lines.join('\n'), 'utf8').digest('hex').slice(0, 16);

const units = JSON.parse(fs.readFileSync(path.join(WORK, 'units.json'), 'utf8'));
const tr = {};
for (const f of fs.readdirSync(path.join(WORK, 'es')).filter((x) => x.endsWith('.json'))) {
  Object.assign(tr, JSON.parse(fs.readFileSync(path.join(WORK, 'es', f), 'utf8')));
}

const out = {};
let n = 0, dup = 0;
for (const u of units) {
  const es = tr[u.id];
  if (!es) continue;
  const k = key(u.lines);
  if (out[k]) { dup++; continue; }
  out[k] = es;
  n++;
}

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(out, null, 1), 'utf8');
console.log('exportadas', n, 'entradas únicas (', dup, 'repetidas omitidas ) ->', OUT);
