# Higiene continua del repo — el anexo operativo

Este anexo es la mitad que se consulta MIENTRAS ejecutas. La mitad que
cambia decisiones vive en el `SKILL.md` de `desarrollo-riguroso`,
sección «Higiene continua del repo», y hay que leerla primero: sin ella
esto es una caja de herramientas sin criterio.

## Leer la salida de una herramienta es una fuente de defectos, no un detalle

Tres lecturas equivocadas del mismo dato en un día, **y las tres subestimaban**. Una
expresión regular sobre el texto con colores dio 1 de 40. Leyendo la salida estándar, el
texto de errores venía pegado al final del informe y lo reventaba, dando 0 de 40. Y el
puntaje no se llamaba como yo creía, dando 0 otra vez.

- **Pide el informe en formato de datos y a un ARCHIVO**, nunca por la salida estándar,
  que viene mezclada con la de errores.
- **Una medición que falla dice DESCONOCIDA, jamás cero.** Un cero silencioso se lee como
  «está limpio», que es la conclusión contraria. En un portón, un fallo de lectura mata el
  portón en vez de devolver un número inventado.
- **Compara contra la herramienta cruda antes de creerle a tu lector.** Si tu informe dice
  1 y la herramienta dice 40, el defecto es tuyo.

## Antes de medir, acota. Una medición que incluye lo que no puedes arreglar no sirve

La duplicación de un repo daba 31,92 por ciento y tapaba la real, que era 4,43, porque
contaba archivos capturados de un sitio externo que se guardan como evidencia de pruebas.
Y el detector de código muerto marcaba medio repositorio, porque no encontraba el punto de
entrada.

**Cuando un medidor dé una cifra escandalosa, la primera hipótesis es que está midiendo
mal, no que el código esté podrido.** Cuando la cifra cae de 15 hallazgos a 4 al arreglar
la configuración, esos 11 eran ruido que habría costado una tarde.

Causa concreta que conviene tener a mano: **un BOM al inicio de un archivo de
configuración.** El programa principal lo tolera y la siguiente herramienta falla al
leerlo. Un BOM no rompe nada visible, rompe al próximo programa que lea el archivo.

## La unidad accionable no siempre es la que reporta la herramienta

Los detectores de clones reportan **parejas**. La unidad sobre la que uno actúa es la
**familia**, o sea todos los sitios que comparten el mismo fragmento. Cuatro copias
producen seis parejas y se leen como seis problemas distintos.

El informe agrupa las parejas en familias, ordena por `(sitios - 1) x líneas`, que es lo
que de verdad se ahorra, e **imprime el fragmento compartido**, para no tener que abrir
cuatro archivos y adivinar de qué se trata.

Regla general más allá de los clones: **antes de mostrar la salida de una herramienta,
pregúntate cuál es la unidad sobre la que se decide, y agrupa hasta llegar a ella.**

## Cualquier lenguaje: se adopta la FUNCIÓN, no el nombre de la herramienta

Nada de esto pertenece a un lenguaje. Cada pieza es una **función** y en cada lenguaje hay
algo que la cumple. **Al entrar a un repo, lo primero es inventariar qué lenguajes tiene
de verdad, y buscar el equivalente de cada función para cada uno.** Un repo políglota con
instrumentos en un solo lenguaje deja el resto sin vigilancia y da tranquilidad falsa, que
es peor que no medir.

| Función | JavaScript y TypeScript | Python | Rust | Go | Java y Kotlin | C y C++ | Varios lenguajes |
|---|---|---|---|---|---|---|---|
| Formato y estilo | Biome | Ruff format | rustfmt | gofmt | ktlint, spotless | clang-format | pre-commit |
| Complejidad excesiva | Biome | Ruff, radon | clippy | gocyclo | detekt, PMD | clang-tidy | lizard |
| Código duplicado | jscpd | jscpd | jscpd | dupl | PMD CPD | PMD CPD | jscpd, PMD CPD |
| Declaraciones muertas | knip | vulture, deptry | cargo-udeps | deadcode | (IDE) | cppcheck | — |
| Grafo de dependencias | dependency-cruiser | pydeps | cargo-modules | go mod graph | jdeps | include-what-you-use | — |
| Vulnerabilidades de terceros | npm audit | pip-audit | cargo audit | govulncheck | OWASP DC | — | Dependabot, Snyk |
| Camino del dato | CodeQL | CodeQL, bandit | cargo geiger | CodeQL | CodeQL | CodeQL | Semgrep |

Antes de dar una fila por buena, **verifica que la herramienta exista y corra hoy en ese
proyecto**, porque esta tabla envejece. La forma de verificarlo es correrla, no leer su
página.

El trinquete es agnóstico por construcción: cada métrica es una función que recibe una
carpeta y devuelve un número donde menos es mejor. Agregar un lenguaje es agregar una
entrada a esa lista.

## Cómo se instala esto en un repo que no lo tiene, en orden

1. **Inventaria los lenguajes reales**, contando archivos, no leyendo el README.
2. **Elige un equivalente por función y por lenguaje**, y corre cada uno una vez para
   confirmar que existe y funciona.
3. **Acota antes de creerle a la primera cifra.** Excluye datos capturados, artefactos y
   dependencias, y declara los puntos de entrada que nadie importa.
4. **Enciende el trinquete** con esas métricas. No exige limpiar nada, solo no empeorar.
5. **Escribe la primera comprobación de clase a partir del último fallo real** que tuvo el
   proyecto. Esta es la que va a encontrar algo.
6. **Prueba cada portón rompiéndolo** y revierte.
7. **Recién ahí mira el informe de oportunidades** y arregla, de a un commit por hallazgo.

El paso 5 es el que se salta todo el mundo, y es el único que atrapa defectos de
comportamiento.

## Lo que NO hace falta, y por qué

La lista canónica de «herramientas para coordinar un ejército de desarrolladores»
(plataformas de calidad, buscadores universales de código, portales de servicios) resuelve
un problema que casi ningún proyecto tiene todavía: **fragmentación del conocimiento entre
muchas personas y muchos repos.** Sus funciones de calidad ya están cubiertas por
instrumentos locales, gratis y de segundos, y su regla estrella («que ningún cambio empeore
el código») es exactamente el trinquete, en una versión más débil porque su umbral se
guarda.

El criterio para adoptar una de ellas es una pregunta concreta, no el prestigio de la
herramienta: **¿hay hoy alguien que no encuentra el código que necesita?** Si la respuesta
es no, es infraestructura que hay que mantener sin nadie que la use. El día que sean varios
repos y varias personas, primero el buscador y mucho después el portal.
