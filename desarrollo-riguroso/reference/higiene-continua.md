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

Y la causa concreta que más veces está detrás de una cifra escandalosa es **un BOM al
inicio de un archivo de configuración**, porque hace fallar la lectura de esa configuración
sin que nadie lo note.

Un BOM (marca de orden de bytes) son tres bytes invisibles, `EF BB BF`, que algunos
editores de Windows escriben al principio de un archivo de texto. **El programa que
escribió el archivo lo tolera y el siguiente que lo lea falla**, con un error que habla de
un carácter inesperado delante de la primera llave. Un BOM no rompe nada visible, rompe al
próximo programa que lea el archivo.

Se detecta leyendo el archivo como bytes y comparando los tres primeros; si están, se
reescribe sin ellos. Los editores lo ofrecen como «guardar sin BOM», y en Windows el
culpable habitual es `Out-File`, que lo antepone por defecto.

## La unidad accionable no siempre es la que reporta la herramienta

Los detectores de clones reportan **parejas**. La unidad sobre la que uno actúa es la
**familia**, o sea todos los sitios que comparten el mismo fragmento. Cuatro copias
producen seis parejas y se leen como seis problemas distintos. El costo de esa lectura es
doble. el informe parece más largo de lo que es, así que se abandona antes, y quien intenta
arreglarlo va sitio por sitio en vez de escribir el ayudante único que resuelve los cuatro
de una vez.

El informe agrupa las parejas en familias, las ordena por `(sitios - 1) x líneas`, e
**imprime el fragmento compartido**, para no tener que abrir cuatro archivos y adivinar de
qué se trata.

Esa resta es lo que de verdad se ahorra. De N copias sobrevive una, la que queda dentro del
ayudante, así que lo que desaparece son las otras N menos 1.

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

## Cómo se escribe una comprobación de clase

Es el paso que encuentra defectos de verdad, así que va con receta y no con consejo.

**Cuándo se escribe.** Justo después de arreglar un defecto, mientras todavía sabes qué
lo hacía posible. No antes, porque no sabrías qué buscar, y no mucho después, porque se
te olvida el patrón exacto.

**Los cinco pasos.**

1. **Nombra el patrón en una frase que hable del CÓDIGO, no del síntoma.** «El informe
   salía incompleto» no sirve. «Se arma el texto a partir de la lista sin paginar»
   sí sirve, porque se puede buscar.
2. **Escribe una prueba normal** en la suite del proyecto. No necesita herramienta nueva:
   lee los archivos fuente con las funciones de archivo del lenguaje, recorre cada línea
   y busca el patrón.
3. **Falla con la lista de sitios culpables, y con el remedio adentro del mensaje.** Un
   fallo que dice «hay 3 problemas» obliga a investigar; uno que dice «estos 3 archivos y
   líneas, usa X en su lugar» se arregla al toque. **Y prueba que ese remedio pase el
   guardia**, porque un mensaje que enseña una salida que también se rechaza cuesta
   varios intentos a quien lo lee.
4. **Escribe la prueba de que la prueba puede fallar**, en la misma tanda. Corre el
   detector sobre un caso bueno y uno malo escritos a mano, y verifica que distinga. Tiene
   que correr sobre **la misma función** que usa la comprobación, no sobre una copia del
   patrón, o estarás probando una copia sana mientras la real está rota.
5. **Mete el defecto a propósito en el repo, confirma el rojo, y revierte.** Los pasos 4
   y 5 no se sustituyen entre sí: el 4 prueba el detector, el 5 prueba que está enchufado.

**Qué esperar.** La primera vez que corre suele encontrar más sitios de los que
arreglaste, porque el patrón se copió entre archivos sin que nadie lo decidiera. Eso es
lo que la hace rentable. Si encuentra exactamente uno, revisa que de verdad esté
recorriendo todos los archivos.

**Su límite, que hay que respetar.** Lee texto, no ejecuta nada, así que no ve lo que solo
existe en tiempo de ejecución y se puede burlar con una variable intermedia. No es una
valla contra un adversario, es una red contra la repetición distraída, que es de donde
sale la mayoría de estos defectos.

## El trinquete y el informe no existen todavía: los escribes tú

Los dos son scripts propios de unas 100 líneas, no herramientas que se instalen. Nadie
publica un trinquete que sirva, porque las métricas y los comandos cambian con cada
proyecto. Acá va el núcleo de cada uno, que es la parte que cuesta pensar; el resto es
imprimir.

### El núcleo del trinquete

Una métrica es un nombre y una función que recibe una carpeta y devuelve un número donde
menos es mejor. Nada más.

    METRICAS = [
      { nombre: 'funciones muy complejas', medir: (dir) => contar(...) },
      { nombre: 'codigo duplicado',        medir: (dir) => porcentaje(...) },
    ]

El bucle completo es este, y lo único delicado son los dos comentarios.

    base = git merge-base <rama-por-defecto> HEAD
    dir  = crear un arbol de trabajo temporal en ese commit
    copiar al dir los archivos de CONFIGURACION del arbol actual
      // son los que le dicen a cada instrumento COMO medir, y los
      // conoces porque los escribiste tu en el paso 3 del arranque: el
      // del linter, el del detector de clones, el del detector de
      // codigo muerto, y el del compilador si define que se compila
      // porque si el arbol viejo midiera con su propia configuracion
      // serian 2 varas distintas, y estrenar una regla se leeria como
      // que el codigo empeoro
    para cada metrica:
      ahora = medir(arbol de trabajo)
      antes = medir(dir)
      si ahora > antes -> ROJO
    borrar el arbol temporal
      // en un finally, o cada corrida deja basura en el disco

Tres cosas que hay que respetar o el trinquete miente.

- **La configuración sale siempre del árbol actual**, nunca del viejo.
- **Un fallo de lectura mata el portón**, nunca devuelve cero. Un cero se lee como
  «limpio» y es la conclusión contraria.
- **La línea base no se guarda en ningún archivo.** Si existiera un número editable, el
  mantenedor lo sube en el mismo commit que lo rompe.

### El núcleo del informe de oportunidades

El informe no decide nada, así que puede ser tosco. Corre los instrumentos, agrupa y
ordena.

    1. correr el detector de clones pidiendo su salida en formato de datos
    2. agrupar las PAREJAS en FAMILIAS
         (une A-B y B-C en {A,B,C}; cualquier union-find o un mapa de conjuntos sirve)
    3. ordenar por (sitios - 1) x lineas, que es lo que de verdad se ahorra
    4. imprimir, por familia, el ahorro, cada ruta con su linea, y el
       FRAGMENTO compartido, para no tener que abrir 4 archivos y adivinar
    5. debajo, la lista de funciones sobre el umbral de complejidad y la de
       declaraciones sin usar, cada una con ruta y linea

Y cerrar con una frase que diga que es una lista y no una orden, por ejemplo esta, que es
la que usa el informe real: «Esto es una LISTA, no una orden. Cada arreglo va en su propio
commit, y el trinquete ya impide que estos números empeoren mientras tanto.» Un informe que
se lee como mandato se termina apagando.

## Cómo se instala esto en un repo que no lo tiene, en orden

1. **Inventaria los lenguajes reales**, contando archivos, no leyendo el README.
2. **Elige un equivalente por función y por lenguaje**, y corre cada uno una vez para
   confirmar que existe y funciona.
3. **Acota antes de creerle a la primera cifra.** Excluye datos capturados, artefactos y
   dependencias, y declara los puntos de entrada que nadie importa.
4. **Escribe y enciende el trinquete** con esas métricas (su núcleo está en la sección
   anterior; son unas 100 líneas y no hay nada que instalar). No exige limpiar nada, solo
   no empeorar.
5. **Escribe la primera comprobación de clase a partir del último fallo real** que tuvo el
   proyecto. Esta es la que va a encontrar algo.
6. **Prueba cada portón rompiéndolo** y revierte.
7. **Recién ahí escribe el informe de oportunidades y míralo** (su núcleo también está
   arriba), y arregla de a un commit por hallazgo.

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
