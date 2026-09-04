$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$parche = $PSScriptRoot
$juego  = Split-Path -Parent $parche
$backup = Join-Path $juego '_original_ingles'

Write-Host ''
Write-Host '  CONDOMINIUM: NO EXIT — Volver a la versión inglesa' -ForegroundColor Red
Write-Host '  =================================================='
Write-Host ''

if (-not (Test-Path $backup)) {
    Write-Host '  [X] No hay copia de seguridad (_original_ingles).' -ForegroundColor Yellow
    Write-Host '      Si la borraste, vuelve a descomprimir la demo original.'
    Write-Host ''
    Read-Host '  Pulsa Intro para salir'
    exit 1
}

$archivos = Get-ChildItem -Path $backup -Recurse -File
$n = 0
foreach ($f in $archivos) {
    $rel     = $f.FullName.Substring($backup.Length + 1)
    $destino = Join-Path $juego (Join-Path 'www' $rel)
    New-Item -ItemType Directory -Force -Path (Split-Path $destino) | Out-Null
    Copy-Item $f.FullName $destino -Force
    $n++
}

Write-Host "  ✔ Restaurados $n archivos originales." -ForegroundColor Green
Write-Host '    El juego vuelve a estar en inglés.'
Write-Host ''
Read-Host '  Pulsa Intro para salir'
