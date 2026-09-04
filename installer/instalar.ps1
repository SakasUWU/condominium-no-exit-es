$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$parche = $PSScriptRoot
$juego  = Split-Path -Parent $parche
$origen = Join-Path $parche 'www'
$backup = Join-Path $juego  '_original_ingles'

Write-Host ''
Write-Host '  CONDOMINIUM: NO EXIT — Traducción al español' -ForegroundColor Red
Write-Host '  ============================================'
Write-Host ''

if (-not (Test-Path (Join-Path $juego 'Game.exe'))) {
    Write-Host '  [X] No encuentro Game.exe.' -ForegroundColor Yellow
    Write-Host ''
    Write-Host '      Descomprime el ZIP DENTRO de la carpeta del juego,'
    Write-Host '      la que contiene Game.exe, y vuelve a ejecutar Instalar.bat.'
    Write-Host ''
    Read-Host '  Pulsa Intro para salir'
    exit 1
}
if (-not (Test-Path $origen)) {
    Write-Host '  [X] Falta la carpeta _parche\www. Vuelve a descomprimir el ZIP entero.' -ForegroundColor Yellow
    Read-Host '  Pulsa Intro para salir'
    exit 1
}

$archivos = Get-ChildItem -Path $origen -Recurse -File
Write-Host "  Archivos del parche: $($archivos.Count)"
Write-Host ''

# --- copia de seguridad de los originales (solo la primera vez) ---
if (Test-Path $backup) {
    Write-Host '  - Ya hay una copia de seguridad de la version inglesa; se conserva.'
} else {
    Write-Host '  - Guardando los originales en _original_ingles\ ...'
    $n = 0
    foreach ($f in $archivos) {
        $rel     = $f.FullName.Substring($origen.Length + 1)
        $destino = Join-Path $juego (Join-Path 'www' $rel)
        if (Test-Path $destino) {
            $guardar = Join-Path $backup $rel
            New-Item -ItemType Directory -Force -Path (Split-Path $guardar) | Out-Null
            Copy-Item $destino $guardar -Force
            $n++
        }
    }
    Write-Host "    $n archivos respaldados."
}

# --- instalar ---
Write-Host '  - Instalando la traducción...'
$n = 0
foreach ($f in $archivos) {
    $rel     = $f.FullName.Substring($origen.Length + 1)
    $destino = Join-Path $juego (Join-Path 'www' $rel)
    New-Item -ItemType Directory -Force -Path (Split-Path $destino) | Out-Null
    Copy-Item $f.FullName $destino -Force
    $n++
}

Write-Host ''
Write-Host "  ✔ Listo: $n archivos instalados." -ForegroundColor Green
Write-Host '    Abre Game.exe y disfrútalo.'
Write-Host ''
Write-Host '    Para volver al inglés, ejecuta Desinstalar.bat.'
Write-Host ''
Read-Host '  Pulsa Intro para salir'
