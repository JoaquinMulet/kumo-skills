import argparse
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MODELO = "opencode-go/deepseek-v4.1-flash"


def avisar(texto):
    print(texto, file=sys.stderr, flush=True)


def main():
    p = argparse.ArgumentParser(description="Lanza un lector frio con DeepSeek por OpenCode Go, sin gastar cuota de Claude.")
    p.add_argument("--documento", required=True, help="Archivo de texto o Markdown que el lector recibe, solo ese.")
    p.add_argument("--encargo", required=True, help="Archivo con el rol, la tarea, las preguntas y lo que debe reportar.")
    p.add_argument("--salida", required=True, help="Archivo donde queda la respuesta completa del lector.")
    p.add_argument("--modelo", default=MODELO)
    p.add_argument("--plazo", type=int, default=600, help="Segundos antes de cortar la llamada.")
    a = p.parse_args()

    opencode = shutil.which("opencode")
    if not opencode:
        avisar("No encontre opencode en el PATH. Instalalo o usa el lector con Agent y modelo haiku.")
        return 2
    documento = Path(a.documento).resolve()
    encargo = Path(a.encargo).read_text(encoding="utf-8")
    salida = Path(a.salida).resolve()
    registro = salida.with_suffix(salida.suffix + ".log")

    with tempfile.TemporaryDirectory(prefix="lector_") as carpeta:
        copia = Path(carpeta) / documento.name
        shutil.copyfile(documento, copia)
        mensaje = encargo + f"\n\nEl documento esta adjunto y tambien en esta carpeta como {documento.name}. Lee solo ese archivo. No modifiques nada."
        comando = [opencode, "run", mensaje, "--pure", "--agent", "plan", "-m", a.modelo, "-f", str(copia)]
        avisar(f"Lector {a.modelo} leyendo {documento.name}. Suele tardar de 30 segundos a 5 minutos.")
        inicio = time.time()
        try:
            r = subprocess.run(comando, cwd=carpeta, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=a.plazo)
        except subprocess.TimeoutExpired:
            avisar(f"El lector no termino en {a.plazo} segundos.")
            registro.write_text(f"plazo agotado tras {a.plazo} s\n", encoding="utf-8")
            return 3
        segundos = round(time.time() - inicio)
        registro.write_text(f"modelo {a.modelo}\ncodigo {r.returncode}\nsegundos {segundos}\n\n{r.stderr}", encoding="utf-8")
        texto = r.stdout.strip()
        if r.returncode != 0 or len(texto) < 50:
            avisar(f"El lector fallo o respondio casi nada. Codigo {r.returncode}. Revisa {registro}.")
            return 1
        salida.write_text(texto + "\n", encoding="utf-8")
        avisar(f"Listo en {segundos} segundos. Respuesta en {salida}, {len(texto.split())} palabras.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
