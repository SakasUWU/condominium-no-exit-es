// Extrae unidades de traducción (bloques de mensaje, opciones, campos de BBDD)
// y las vuelve a inyectar en los .json de RPG Maker MV.
const fs = require('fs');
const path = require('path');

const DB_FIELDS = ['name', 'nickname', 'profile', 'description', 'message1', 'message2', 'message3', 'message4'];
const DB_FILES = ['Actors.json', 'Classes.json', 'Items.json', 'Skills.json', 'Weapons.json', 'Armors.json', 'Enemies.json', 'States.json'];

// --- recorrido de listas de comandos ------------------------------------
// Devuelve [{ owner, key, list }] para cada lista de comandos del archivo.
function findLists(json, out = [], trail = []) {
  if (Array.isArray(json)) {
    json.forEach((v, i) => { if (v && typeof v === 'object') findLists(v, out, trail.concat(i)); });
  } else if (json && typeof json === 'object') {
    for (const k of Object.keys(json)) {
      const v = json[k];
      if (k === 'list' && Array.isArray(v)) out.push({ holder: json, path: trail.concat('list') });
      else if (v && typeof v === 'object') findLists(v, out, trail.concat(k));
    }
  }
  return out;
}

function extractFile(file, json, push) {
  for (const { holder, path: p } of findLists(json, [], [])) {
    const list = holder.list;
    const key = p.join('/');
    let face = '';
    for (let i = 0; i < list.length; i++) {
      const c = list[i];
      if (c.code === 101) { face = c.parameters[0] || ''; continue; }
      if (c.code === 401) {
        const start = i;
        const lines = [];
        while (i < list.length && list[i].code === 401) { lines.push(list[i].parameters[0]); i++; }
        i--;
        push({ type: 'message', file, list: key, start, count: lines.length, face, lines });
        continue;
      }
      if (c.code === 405) {
        const start = i;
        const lines = [];
        while (i < list.length && list[i].code === 405) { lines.push(list[i].parameters[0]); i++; }
        i--;
        push({ type: 'scroll', file, list: key, start, count: lines.length, lines });
        continue;
      }
      if (c.code === 102) {
        push({ type: 'choice', file, list: key, start: i, lines: c.parameters[0].slice() });
      }
      if (c.code === 320 || c.code === 324 || c.code === 325) {
        push({ type: 'cmdparam', file, list: key, start: i, param: 1, lines: [c.parameters[1]] });
      }
    }
  }
}

function extract(dataDir) {
  const units = [];
  let id = 0;
  const push = (u) => {
    const has = (u.lines || []).some((s) => typeof s === 'string' && s.trim());
    if (!has) return;
    u.id = ++id;
    units.push(u);
  };

  const files = fs.readdirSync(dataDir).filter((f) => f.endsWith('.json'));
  for (const f of files) {
    let json;
    try { json = JSON.parse(fs.readFileSync(path.join(dataDir, f), 'utf8')); } catch (e) { continue; }

    if (/^Map\d+\.json$/.test(f) || f === 'CommonEvents.json' || f === 'Troops.json') {
      extractFile(f, json, push);
      if (json.displayName) push({ type: 'field', file: f, ptr: '/displayName', lines: [json.displayName] });
      continue;
    }
    if (f === 'MapInfos.json') {
      json.forEach((mi, i) => { if (mi && mi.name) push({ type: 'field', file: f, ptr: `/${i}/name`, lines: [mi.name] }); });
      continue;
    }
    if (f === 'System.json') {
      push({ type: 'field', file: f, ptr: '/gameTitle', lines: [json.gameTitle] });
      push({ type: 'field', file: f, ptr: '/currencyUnit', lines: [json.currencyUnit] });
      for (const k of ['armorTypes', 'weaponTypes', 'skillTypes', 'equipTypes', 'elements']) {
        (json[k] || []).forEach((v, i) => push({ type: 'field', file: f, ptr: `/${k}/${i}`, lines: [v] }));
      }
      const t = json.terms || {};
      for (const k of ['basic', 'commands', 'params']) {
        (t[k] || []).forEach((v, i) => push({ type: 'field', file: f, ptr: `/terms/${k}/${i}`, lines: [v] }));
      }
      Object.keys(t.messages || {}).forEach((k) => push({ type: 'field', file: f, ptr: `/terms/messages/${k}`, lines: [t.messages[k]] }));
      continue;
    }
    if (DB_FILES.includes(f)) {
      json.forEach((o, i) => {
        if (!o) return;
        for (const k of DB_FIELDS) {
          if (typeof o[k] === 'string' && o[k].trim()) {
            push({ type: 'field', file: f, ptr: `/${i}/${k}`, lines: [o[k]] });
          }
        }
      });
      continue;
    }
  }
  return units;
}

// --- reinyección ---------------------------------------------------------
function getByPath(json, p) {
  let cur = json;
  for (const seg of p.split('/')) cur = cur[/^\d+$/.test(seg) ? Number(seg) : seg];
  return cur;
}
function setByPtr(json, ptr, value) {
  const segs = ptr.split('/').filter(Boolean);
  let cur = json;
  for (let i = 0; i < segs.length - 1; i++) cur = cur[/^\d+$/.test(segs[i]) ? Number(segs[i]) : segs[i]];
  const last = segs[segs.length - 1];
  cur[/^\d+$/.test(last) ? Number(last) : last] = value;
}

function apply(dataDir, outDir, units, translations) {
  fs.mkdirSync(outDir, { recursive: true });
  const byFile = {};
  for (const u of units) (byFile[u.file] = byFile[u.file] || []).push(u);

  const stats = { files: 0, units: 0, missing: 0 };
  for (const file of Object.keys(byFile)) {
    const json = JSON.parse(fs.readFileSync(path.join(dataDir, file), 'utf8'));
    // Editar de atrás hacia delante: insertar/quitar líneas desplaza índices.
    const us = byFile[file].slice().sort((a, b) => {
      if (a.list !== b.list) return String(b.list).localeCompare(String(a.list));
      return (b.start || 0) - (a.start || 0);
    });
    let touched = false;
    for (const u of us) {
      const es = translations[u.id];
      if (!es) { stats.missing++; continue; }
      stats.units++;
      touched = true;
      if (u.type === 'field') { setByPtr(json, u.ptr, es[0]); continue; }
      const list = getByPath(json, u.list);
      if (u.type === 'message' || u.type === 'scroll') {
        const code = u.type === 'message' ? 401 : 405;
        const indent = list[u.start].indent;
        const cmds = es.map((s) => ({ code, indent, parameters: [s] }));
        list.splice(u.start, u.count, ...cmds);
      } else if (u.type === 'choice') {
        const cmd = list[u.start];
        const old = cmd.parameters[0].slice();
        cmd.parameters[0] = es.slice();
        // Actualizar las etiquetas de las ramas 402 correspondientes
        let depth = 0;
        for (let i = u.start + 1; i < list.length; i++) {
          const c = list[i];
          if (c.code === 402 && depth === 0) {
            const idx = c.parameters[0];
            if (idx >= 0 && idx < es.length) c.parameters[1] = es[idx];
          } else if (c.code === 404 && depth === 0) break;
          else if (c.code === 102) depth++;
          else if (c.code === 404 && depth > 0) depth--;
        }
      } else if (u.type === 'cmdparam') {
        list[u.start].parameters[u.param] = es[0];
      }
    }
    if (touched) { fs.writeFileSync(path.join(outDir, file), JSON.stringify(json), 'utf8'); stats.files++; }
  }
  return stats;
}

module.exports = { extract, apply };

if (require.main === module) {
  const [cmd, ...rest] = process.argv.slice(2);
  if (cmd === 'extract') {
    const units = extract(rest[0]);
    fs.writeFileSync(rest[1], JSON.stringify(units, null, 1), 'utf8');
    const words = units.reduce((a, u) => a + u.lines.join(' ').split(/\s+/).filter(Boolean).length, 0);
    const byType = {};
    units.forEach((u) => { byType[u.type] = (byType[u.type] || 0) + 1; });
    console.log('unidades:', units.length, 'palabras:', words, byType);
  }
}
