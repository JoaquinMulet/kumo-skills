#!/usr/bin/env python3
"""Extrae MECANICAMENTE los turnos del usuario de una transcripcion de Claude Code.

Por que existe: el juez frio de la retro no puede recibir la lista de correcciones que ya
curo el agente contaminado — heredaria su omision y validaria felizmente solo lo que si
subio. Tampoco conviene darle la sesion entera: eso lo vuelve a contaminar con el
razonamiento del que audita. La extraccion mecanica de los turnos del usuario es el unico
punto medio que no depende de la buena fe de nadie.

Espera: la ruta de un .jsonl de transcripcion. Las de Claude Code viven en
  ~/.claude/projects/<slug-del-proyecto>/<session-id>.jsonl
y la de la sesion en curso es la que tiene el mtime mas reciente.

Devuelve: los turnos del usuario en orden, numerados, en stdout (o al archivo de -o).
Filtra los mensajes que no escribio la persona: resultados de tools, recordatorios del
sistema y salida de hooks, que en el formato viven bajo el mismo type 'user'.

Uso:
    uv run python scripts/extraer-turnos-usuario.py <transcripcion.jsonl> [-o turnos.md]
    uv run python scripts/extraer-turnos-usuario.py --ultima          # busca la mas reciente

Sale != 0 con mensaje accionable si la ruta no existe, no es .jsonl legible, o no hay
turnos: cero turnos es senal de instrumento roto (formato cambiado), no de sesion vacia.
"""
import argparse
import json
import os
import sys
import glob

# Marcas de contenido inyectado por el harness, no escrito por la persona. Se buscan en el
# ARRANQUE del texto (los primeros 200 chars) porque un turno legitimo puede citarlas mas
# adelante — el usuario pega bloques de sesiones anteriores con frecuencia.
VENTANA_MARCA = 200
MARCAS_HARNESS = (
    "<system-reminder>",
    "<command-name>",
    "<local-command-stdout>",
    "Caveat: The messages below",
    "hook success:",
    "hook feedback:",
    # inyecciones que tambien viajan como queue-operation/enqueue:
    "<task-notification>",          # aviso de subagente terminado
    "[SYSTEM NOTIFICATION",         # envoltorio de notificaciones del harness
    "Base directory for this skill:",  # cuerpo de una skill invocada
)


def texto_del_turno(registro):
    """Devuelve el texto que escribio la persona, o None si el registro no es un turno suyo."""
    # Mensajes enviados A MITAD DE TURNO: el harness los adjunta al siguiente
    # tool_result (donde el filtro de abajo los bota, con razon), pero quedan
    # LIMPIOS en el registro queue-operation/enqueue. Sin esta rama, toda
    # correccion dicha mientras el agente trabajaba es invisible para el juez
    # frio de la retro (descubierto el 2026-08-06: dos correcciones reales del
    # usuario no aparecian entre los turnos extraidos y el juez las declaro
    # de origen no rastreable). Como un mensaje encolado puede ademas llegar
    # como turno 'user' normal, main() deduplica textos exactos.
    if registro.get("type") == "queue-operation":
        if registro.get("operation") != "enqueue":
            return None
        texto = registro.get("content")
        if not isinstance(texto, str):
            return None
        texto = texto.strip()
        if not texto or any(m in texto[:VENTANA_MARCA] for m in MARCAS_HARNESS):
            return None
        return texto
    if registro.get("type") != "user":
        return None
    contenido = registro.get("message", {}).get("content")
    if isinstance(contenido, str):
        texto = contenido
    elif isinstance(contenido, list):
        # los bloques tool_result se descartan: no los escribio la persona
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in contenido):
            return None
        texto = " ".join(
            b.get("text", "") for b in contenido
            if isinstance(b, dict) and b.get("type") == "text"
        )
    else:
        return None
    texto = texto.strip()
    if not texto:
        return None
    arranque = texto[:VENTANA_MARCA]
    if any(m in arranque for m in MARCAS_HARNESS):
        return None
    return texto


def transcripcion_mas_reciente():
    patron = os.path.expanduser("~/.claude/projects/*/*.jsonl")
    archivos = glob.glob(patron)
    if not archivos:
        return None
    return max(archivos, key=os.path.getmtime)


def main():
    # En Windows stdout es cp1252 por default y revienta con UnicodeEncodeError en la primera
    # flecha o comilla tipografica de la transcripcion. Sin esto el script "existe, esta
    # documentado y falla" en la mitad de las maquinas de Kumo.
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass  # flujo redirigido o Python sin reconfigure: seguimos igual

    ap = argparse.ArgumentParser(description="Extrae los turnos del usuario de una transcripcion.")
    ap.add_argument("transcripcion", nargs="?", help="ruta al .jsonl")
    ap.add_argument("--ultima", action="store_true", help="usar la transcripcion mas reciente")
    ap.add_argument("-o", "--salida", help="archivo de salida (default: stdout)")
    args = ap.parse_args()

    ruta = args.transcripcion
    if args.ultima and not ruta:
        ruta = transcripcion_mas_reciente()
        if not ruta:
            print("no encontre ninguna transcripcion en ~/.claude/projects/*/*.jsonl — "
                  "pasa la ruta a mano", file=sys.stderr)
            return 2
        print(f"# transcripcion: {ruta}", file=sys.stderr)
    if not ruta:
        ap.print_usage(sys.stderr)
        print("falta la ruta del .jsonl (o usa --ultima)", file=sys.stderr)
        return 2
    if not os.path.isfile(ruta):
        print(f"no existe el archivo: {ruta}", file=sys.stderr)
        return 2

    turnos, lineas_ilegibles = [], 0
    with open(ruta, encoding="utf-8", errors="replace") as fh:
        for linea in fh:
            linea = linea.strip()
            if not linea:
                continue
            try:
                registro = json.loads(linea)
            except json.JSONDecodeError:
                lineas_ilegibles += 1
                continue
            texto = texto_del_turno(registro)
            # dedup exacto: un mensaje encolado (queue-operation) puede llegar
            # tambien como turno 'user' normal; la misma frase dos veces
            # inflaria la senal del juez
            if texto and texto not in turnos:
                turnos.append(texto)

    if lineas_ilegibles:
        print(f"aviso: {lineas_ilegibles} lineas no eran JSON valido y se saltaron", file=sys.stderr)
    if not turnos:
        print("CERO turnos de usuario extraidos — trata esto como instrumento roto "
              "(¿cambio el formato de la transcripcion?), no como sesion vacia.", file=sys.stderr)
        return 1

    partes = [f"## Turno {i} del usuario\n\n{t}\n" for i, t in enumerate(turnos, 1)]
    salida = (f"# Turnos del usuario ({len(turnos)}) — extraidos mecanicamente de "
              f"{os.path.basename(ruta)}\n\n" + "\n".join(partes))
    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as fh:
            fh.write(salida)
        print(f"{len(turnos)} turnos escritos en {args.salida}")
    else:
        sys.stdout.write(salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
