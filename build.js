// Genera el parche completo en build/ a partir de tu copia del juego.
//
//   node build.js [--game="C:/ruta/a/condominium-demo-win-en"] [--skip-images]
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const skipImages = process.argv.includes('--skip-images');
const gameArg = process.argv.find((a) => a.startsWith('--game=')) || '';

function run(cmd, args, label) {
  process.stdout.write(`\n▶ ${label}\n`);
  execFileSync(cmd, args, { cwd: ROOT, stdio: 'inherit' });
}

function python() {
  for (const c of ['python', 'py', 'python3']) {
    try { execFileSync(c, ['--version'], { stdio: 'ignore' }); return c; } catch (e) { /* siguiente */ }
  }
  return null;
}

fs.rmSync(path.join(ROOT, 'build'), { recursive: true, force: true });

run(process.execPath, ['tools/apply-text.js', gameArg].filter(Boolean), 'Texto (diálogos, objetos, menús)');

if (skipImages) {
  console.log('\n(imágenes omitidas por --skip-images)');
} else {
  const py = python();
  if (!py) {
    console.log('\nNo se ha encontrado Python: se omiten las imágenes.');
    console.log('Instala Python 3 y Pillow (pip install pillow numpy) y vuelve a ejecutar.');
  } else {
    run(process.execPath, ['tools/images.js', 'decrypt', gameArg].filter(Boolean), 'Descifrando imágenes');
    const scripts = ['img_clean_plates.py', 'img_title.py', 'img_notify.py', 'img_menu.py', 'img_guides.py', 'img_guide1.py',
                     'img_scenes.py', 'img_phone.py', 'img_messages.py', 'img_messages2.py',
                     'img_misc.py', 'img_credits.py', 'img_demoend.py', 'img_riophone.py'];
    for (const s of scripts) {
      process.stdout.write(`\n▶ ${s}\n`);
      execFileSync(py, [path.join('tools', s)], {
        cwd: ROOT, stdio: 'inherit', env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
      });
    }
    run(process.execPath, ['tools/images.js', 'encrypt', gameArg].filter(Boolean), 'Cifrando imágenes');
  }
}

fs.copyFileSync(path.join(ROOT, 'docs', 'LEEME-parche.txt'), path.join(ROOT, 'build', 'LEEME.txt'));

let n = 0;
(function count(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    if (e.isDirectory()) count(path.join(d, e.name)); else n++;
  }
})(path.join(ROOT, 'build'));

console.log(`\n✔ Parche listo en build/  (${n} archivos)`);
console.log('  Copia el contenido de build/ sobre la carpeta del juego.');
