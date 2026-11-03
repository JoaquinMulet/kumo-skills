#!/usr/bin/env bash
# Compila un documento LaTeX 3 veces y comprueba que el PDF salió entero.
#
# Uso: bash scripts/compilar.sh documento.tex [carpeta-de-compilacion]
#
# Hace 5 cosas:
# 0. Se niega a compilar si algún .tex de la carpeta trae los bytes de control 7, 8 o 12.
# 1. Quita del PATH, solo para este comando, toda entrada que termine en un archivo cl.exe.
#    En la máquina de Kumo el PATH tiene esa entrada rota y MiKTeX se atora con ella.
# 2. Corre pdflatex 3 veces, porque el índice y «página X de Y» necesitan 2 pasadas extra.
# 3. Da el PDF por bueno solo si el log dice «Output written» y PyMuPDF cuenta páginas. El código
#    de salida de MiKTeX no sirve. Ha salido con 1 dejando un PDF correcto, y con PDF cortado.
# 4. Copia el PDF junto al .tex y cuenta los Overfull del log.
#
# Variable PDFLATEX para otra instalación. Por defecto busca pdflatex en el PATH y después la
# ruta de MiKTeX del usuario en Windows.
set -u
TEX="${1:?Falta el archivo .tex}"
DIR="$(cd "$(dirname "$TEX")" && pwd)"
NOMBRE="$(basename "$TEX" .tex)"
SALIDA="${2:-$DIR/trabajo/compilacion}"
mkdir -p "$SALIDA"

export PATH="$(echo "$PATH" | tr ':' '\n' | grep -v 'cl.exe' | paste -sd:)"
if [ -z "${PDFLATEX:-}" ]; then
  if command -v pdflatex >/dev/null 2>&1; then PDFLATEX=pdflatex
  else PDFLATEX="/c/Users/$USERNAME/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe"; fi
fi

cd "$DIR" || exit 2
# Los bytes 7, 8 y 12 (campana, retroceso y salto de página) aparecen cuando un script escribe
# una barra invertida seguida de a, b o f. LaTeX compila igual y el comando queda roto sin aviso
# (regla del 30 oct 2026). Se cuentan en bytes, en todos los .tex de la carpeta.
CONTROL="$(uv run python -I -c "
import glob
for f in sorted(glob.glob('*.tex')):
    b = open(f, 'rb').read()
    n = sum(b.count(bytes([c])) for c in (7, 8, 12))
    if n:
        print(f, n)
")"
if [ -n "$CONTROL" ]; then
  echo "Hay bytes de control (7, 8 o 12) en el .tex. Repara el texto antes de compilar:" >&2
  echo "$CONTROL" >&2
  exit 1
fi
for i in 1 2 3; do
  echo "Pasada $i de 3 de pdflatex. Cada una tarda de 5 a 40 segundos." >&2
  "$PDFLATEX" -interaction=nonstopmode -halt-on-error -output-directory="$SALIDA" "$NOMBRE.tex" \
    > "$SALIDA/salida_pasada_$i.txt" 2>&1
done

LOG="$SALIDA/$NOMBRE.log"
if ! grep -q "Output written" "$LOG"; then
  echo "El log no dice «Output written». El PDF no sirve. Primeros errores:" >&2
  grep -n "^!" "$LOG" | head -5 >&2
  exit 1
fi
PAGINAS="$(uv run --with pymupdf python -I -c "import pymupdf,sys; print(pymupdf.open(sys.argv[1]).page_count)" "$SALIDA/$NOMBRE.pdf")"
if [ "${PAGINAS:-0}" -lt 1 ]; then
  echo "PyMuPDF no cuenta páginas en el PDF. Está cortado." >&2
  exit 1
fi
cp "$SALIDA/$NOMBRE.pdf" "$DIR/$NOMBRE.pdf"
echo "PDF listo con $PAGINAS páginas en $DIR/$NOMBRE.pdf"
echo "Overfull en el log: $(grep -c 'Overfull' "$LOG")"
echo "Referencias sin resolver: $(grep -c 'undefined' "$LOG")"
