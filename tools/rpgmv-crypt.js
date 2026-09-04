// Descifrado/cifrado de recursos RPG Maker MV (.rpgmvp / .rpgmvo / .rpgmvm)
const fs = require('fs');
const path = require('path');

const HEADER_LEN = 16;
const SIGNATURE = Buffer.from([0x52, 0x50, 0x47, 0x4d, 0x56, 0x00, 0x00, 0x00,
                               0x00, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]);

function keyBytes(key) {
  const b = Buffer.alloc(16);
  for (let i = 0; i < 16; i++) b[i] = parseInt(key.substr(i * 2, 2), 16);
  return b;
}

function decrypt(buf, key) {
  const k = keyBytes(key);
  const body = Buffer.from(buf.slice(HEADER_LEN));
  for (let i = 0; i < 16 && i < body.length; i++) body[i] ^= k[i];
  return body;
}

function encrypt(buf, key) {
  const k = keyBytes(key);
  const body = Buffer.from(buf);
  for (let i = 0; i < 16 && i < body.length; i++) body[i] ^= k[i];
  return Buffer.concat([SIGNATURE, body]);
}

module.exports = { decrypt, encrypt };

if (require.main === module) {
  const [mode, key, src, dst] = process.argv.slice(2);
  const fn = mode === 'dec' ? decrypt : encrypt;
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.writeFileSync(dst, fn(fs.readFileSync(src), key));
  console.log(mode, src, '->', dst);
}
