// Medición de ancho de texto usando las métricas reales del TTF del juego.
const fs = require('fs');

function loadFont(ttfPath) {
  const d = fs.readFileSync(ttfPath);
  const numTables = d.readUInt16BE(4);
  const tables = {};
  for (let i = 0; i < numTables; i++) {
    const o = 12 + 16 * i;
    tables[d.toString('latin1', o, o + 4)] = { off: d.readUInt32BE(o + 8), len: d.readUInt32BE(o + 12) };
  }
  const unitsPerEm = d.readUInt16BE(tables.head.off + 18);
  const numHMetrics = d.readUInt16BE(tables.hhea.off + 34);

  // cmap formato 4
  const c = tables.cmap.off;
  const n = d.readUInt16BE(c + 2);
  let sub = null;
  for (let i = 0; i < n; i++) {
    const off = d.readUInt32BE(c + 4 + 8 * i + 4);
    if (d.readUInt16BE(c + off) === 4) sub = c + off;
  }
  const segX2 = d.readUInt16BE(sub + 6), seg = segX2 / 2;
  const endO = sub + 14, startO = endO + segX2 + 2, deltaO = startO + segX2, rangeO = deltaO + segX2;

  function glyphId(code) {
    for (let i = 0; i < seg; i++) {
      const end = d.readUInt16BE(endO + 2 * i);
      if (code > end) continue;
      const start = d.readUInt16BE(startO + 2 * i);
      if (code < start) return 0;
      const delta = d.readInt16BE(deltaO + 2 * i);
      const rangeOff = d.readUInt16BE(rangeO + 2 * i);
      if (rangeOff === 0) return (code + delta) & 0xFFFF;
      const gi = rangeO + 2 * i + rangeOff + 2 * (code - start);
      if (gi + 1 >= d.length) return 0;
      const g = d.readUInt16BE(gi);
      return g === 0 ? 0 : (g + delta) & 0xFFFF;
    }
    return 0;
  }

  const cache = new Map();
  function advance(code) {
    if (cache.has(code)) return cache.get(code);
    const g = glyphId(code);
    const i = Math.min(g, numHMetrics - 1);
    const adv = d.readUInt16BE(tables.hmtx.off + 4 * i);
    const v = adv / unitsPerEm;
    cache.set(code, v);
    return v;
  }
  return { advance };
}

// Quita códigos de control de RPG Maker MV que no ocupan espacio visible
function stripCodes(s) {
  return s
    .replace(/\\TA\[\d+\]/gi, '')
    .replace(/\\[CNVPI]\[\d+\]/gi, (m) => (/^\\I/i.test(m) ? '　' : ''))  // \i[] dibuja un icono (~32px ≈ 1 em)
    .replace(/\\\{|\\\}/g, '')
    .replace(/\\[.|!><^]/g, '')
    .replace(/\\\$/g, '')
    .replace(/<\/?(CENTER|LEFT|RIGHT|WordWrap)>/gi, '')
    .replace(/\\\\/g, '\\');
}

function measure(font, s, fontSize) {
  const t = stripCodes(s);
  let w = 0;
  for (const ch of t) w += font.advance(ch.codePointAt(0)) * fontSize;
  return Math.round(w);
}

module.exports = { loadFont, measure, stripCodes };
