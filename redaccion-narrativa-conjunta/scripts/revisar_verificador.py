"""Revisa el informe de un verificador de citas contra el documento que leyó.

Un verificador es un agente que leyó 1 documento fuente entero y juzgó cada afirmación de un párrafo. Su informe
es un JSON con la forma que pide `encargo_verificador_de_citas.md`. Este script comprueba 3 cosas que no dependen
del modelo.
1. Que la última frase que el agente dice haber leído esté en el documento, como prueba de que llegó al final.
2. Que cada `frase_fuente` esté en el documento, con los espacios y los apóstrofos normalizados. Un agente puede
   inventar una cita, y una sola cita inventada invalida su informe.
3. Lista cada afirmación que no quedó como `respaldada`, con su problema, para que el autor decida.

Uso:
    uv run python scripts/revisar_verificador.py INFORME.json DOCUMENTO

Sale con código 1 si alguna cita no está en el documento o si falta la prueba de lectura.
"""

import json
import sys
from pathlib import Path

VEREDICTOS = {
    "respaldada",
    "respaldada_con_matiz",
    "no_respaldada",
    "no_esta_en_el_documento",
}


def plano(texto: str) -> str:
    return " ".join(
        texto.replace(chr(8217), "'")
        .replace(chr(8216), "'")
        .replace(chr(0), "")
        .split()
    )


def main() -> int:
    informe = json.loads(Path(sys.argv[1]).read_bytes().decode("utf-8"))
    documento = plano(Path(sys.argv[2]).read_bytes().decode("utf-8", errors="replace"))
    fallas = 0
    lectura = informe.get("prueba_de_lectura", {})
    ultima = plano(str(lectura.get("ultima_frase_del_documento", "")))
    if not lectura.get("lei_todo") or not ultima or ultima not in documento:
        print("FALLA  la prueba de lectura no calza con el documento")
        fallas += 1
    conteo = dict.fromkeys(sorted(VEREDICTOS), 0)
    for a in informe["afirmaciones"]:
        veredicto = a.get("veredicto", "")
        if veredicto not in VEREDICTOS:
            print(
                f"FALLA  afirmación {a.get('n')}: veredicto desconocido «{veredicto}»"
            )
            fallas += 1
            continue
        conteo[veredicto] += 1
        frase = plano(a.get("frase_fuente") or "")
        if frase and frase not in documento:
            print(
                f"FALLA  afirmación {a.get('n')}: la cita no está en el documento «{frase[:70]}»"
            )
            fallas += 1
        if veredicto != "respaldada":
            print(f"{veredicto}  gravedad {a.get('gravedad', '')}")
            print(f"    dice    {a.get('afirmacion', '')}")
            print(f"    problema {a.get('problema', '')}")
            if a.get("cautela_omitida"):
                print(f"    cautela {a['cautela_omitida']}")
    for frase in informe.get("lo_que_el_parrafo_deja_fuera", []):
        print(f"deja fuera  {frase}")
    print()
    print("  ".join(f"{k} {v}" for k, v in conteo.items()))
    print(
        "Todo pasa."
        if not fallas
        else f"{fallas} falla(s) del verificador. Su informe no se usa hasta arreglarlas."
    )
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
