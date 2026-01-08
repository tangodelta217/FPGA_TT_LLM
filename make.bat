@echo off
setlocal

set target=%1
if "%target%"=="" set target=help

if "%target%"=="help" goto :help
if "%target%"=="setup" goto :setup
if "%target%"=="lint" goto :lint
if "%target%"=="test" goto :test
if "%target%"=="demo" goto :demo
if "%target%"=="benchmarks" goto :benchmarks
if "%target%"=="indra-pack" goto :indra_pack
if "%target%"=="wow-audit" goto :wow_audit

:unknown
echo Target no reconocido: %target%
exit /b 1

:help
echo Targets:
echo   setup       Instala dependencias
echo   lint        Ejecuta ruff
echo   test        Ejecuta pytest
echo   demo        Genera evidencia funcional en docs/assets
echo   benchmarks  Ejecuta microbenchmarks CPU
echo   indra-pack  Empaqueta docs/indra y docs/assets
echo   wow-audit   Verifica evidencias minimas
exit /b 0

:setup
python -m pip install -r requirements.txt
exit /b %errorlevel%

:lint
python -m ruff check .
exit /b %errorlevel%

:test
python -m pytest
exit /b %errorlevel%

:demo
python -m scripts.demo_tt
exit /b %errorlevel%

:benchmarks
python -m scripts.bench_tt
exit /b %errorlevel%

:indra_pack
python -m scripts.indra_pack
exit /b %errorlevel%

:wow_audit
python -m scripts.wow_audit
exit /b %errorlevel%
