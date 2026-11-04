# Fase 1: Preparación de los datos

Guía completa para preparar los documentos antes de lanzar el análisis forense.

---

## Paso 1.1: Recopilación de documentos

### Para empresas de EE.UU. (presentaciones ante la SEC)

| Documento | Ubicación | Secciones clave |
|----------|----------|--------------|
| **10-K** | SEC EDGAR | Informe anual completo |
| **Estados financieros** | 10-K, Parte II, Item 8 | Balance, estado de resultados, flujo de caja |
| **MD&A** | 10-K, Parte II, Item 7 | Discusión y análisis de la gerencia |
| **Notas** | Dentro del Item 8 | Notas numeradas (1-30+) |
| **Informe del auditor** | Antes de los estados financieros | Asuntos clave de auditoría |

**Cómo acceder**:
```
1. Go to: https://www.sec.gov/cgi-bin/browse-edgar
2. Search by company name or ticker
3. Filter: Form Type = 10-K
4. Download most recent filing
```

### Para empresas internacionales (IFRS)

| Documento | Nombre típico | Secciones clave |
|----------|--------------|--------------|
| **Informe anual** | Memoria Anual / Annual Report | Paquete completo |
| **EEFF** | Estados Financieros Consolidados | Estados financieros |
| **Notas** | Notas a los Estados Financieros | Notas numeradas |
| **MD&A** | Analisis Razonado | Discusión de la gerencia |
| **Informe del auditor** | Informe del Auditor | Asuntos clave de auditoría |

**Cómo acceder**:
```
1. Company investor relations website
2. Local securities regulator (CMF, SMV, etc.)
3. Stock exchange filings
```

---

## Paso 1.2: Conversión de PDF a Markdown

Si los documentos están en formato PDF:

```
LOAD SKILL: pdf (o PyMuPDF con uv run --with pymupdf, que lee el texto por página)

EXECUTE:
1. Convert Financial Statements PDF
2. Convert MD&A / Analisis Razonado PDF
3. Verify conversion quality (tables, numbers)

OUTPUT:
- {COMPANY}_EEFF_{PERIOD}.md
- {COMPANY}_MDA_{PERIOD}.md
```

### Control de calidad después de la conversión

Verifica que estos elementos se hayan convertido correctamente:
- [ ] Todas las tablas tienen la alineación de columnas correcta
- [ ] Los números son exactos (revisa al azar entre 5 y 10 valores)
- [ ] Se conservan los números de las notas
- [ ] Los encabezados y los cortes de sección son claros
- [ ] No faltan páginas ni secciones

---

## Paso 1.3: Identificar las notas clave

Antes de lanzar los agentes, crea una tabla de mapeo de notas:

### Notas esenciales para detectar manipulaciones contables

| Categoría de datos | Qué buscar | Ubicación en el 10-K | Ubicación en los EEFF |
|---------------|--------------|---------------|---------------|
| **Ingresos** | Política de reconocimiento, ingresos diferidos | Nota "Revenue" o "Summary of Policies" | Nota 3 (Politicas) + Nota 22 |
| **Cuentas por cobrar** | Provisión, antigüedad, castigos | Nota "Accounts Receivable" | Nota 8 |
| **Inventarios** | Valoración, obsolescencia | Nota "Inventory" | Nota 10 |
| **PPE** | Bruto, depreciación acumulada, vidas útiles | Nota "Property, Plant & Equipment" | Nota 14 |
| **Intangibles** | Plusvalía, intangibles adquiridos | Nota "Intangible Assets" | Nota 12-13 |
| **DTA/DTL** | Saldos, provisión de valuación | Nota "Income Taxes" | Nota 15 |
| **Partes relacionadas** | Transacciones, saldos | Nota "Related Party Transactions" | Nota 9 |
| **Segmentos** | Segmentos geográficos y de negocio | Nota "Segment Reporting" | Nota 29 |
| **Compromisos** | Fuera de balance, contingencias | Nota "Commitments and Contingencies" | Nota 32 |
| **Arriendos** | Activos por derecho de uso, pasivos por arrendamiento | Nota "Leases" | Nota 28 |

### Crea la ficha de referencia de notas

```markdown
## {COMPANY} - Note Reference Card

| Category | Note # | Page | Key Data Points |
|----------|--------|------|-----------------|
| Revenue | Note X | p.XX | Policy, deferred rev balance |
| Receivables | Note X | p.XX | Allowance %, aging schedule |
| PPE | Note X | p.XX | Gross, accum depr, additions |
| DTA | Note X | p.XX | Balance, valuation allowance |
| Related Parties | Note X | p.XX | Transaction types, amounts |
| Segments | Note X | p.XX | Revenue by geography |
```

---

## Paso 1.4: Extraer los datos geográficos

Fundamental para el ajuste por inflación de los owner earnings.

### Paso 4.1: Encontrar la información de segmentos

Busca en la nota de información por segmentos:
- Ingresos por región geográfica
- Utilidad operacional por región
- Activos por región

### Paso 4.2: Calcular las ponderaciones de ingresos

Ejemplo:
```
Total Revenue: $1,000M

By Geography:
- Domestic (USA): $600M -> 60%
- Europe: $250M -> 25%
- Latin America: $150M -> 15%
```

### Paso 4.3: Buscar las tasas de inflación

Obtén la inflación anual vigente de cada país:
- EE.UU.: Federal Reserve / BLS
- Chile: INE / Banco Central
- Perú: INEI / BCRP
- Europa: Eurostat

### Paso 4.4: Calcular la inflación combinada

```
Blended Inflation = Sum(Weight_i x Inflation_i)

Example:
- USA (60%): 3.5% -> 2.10%
- Europe (25%): 2.5% -> 0.63%
- LatAm (15%): 5.0% -> 0.75%
--------------------------
Blended: 3.48%
```

### Plantilla de datos geográficos

```markdown
## {COMPANY} - Geographic Inflation Data

| Region | Revenue (M$) | Weight | Local Inflation | Weighted |
|--------|--------------|--------|-----------------|----------|
| {Region 1} | {X} | {X}% | {X.X}% | {X.XX}% |
| {Region 2} | {X} | {X}% | {X.X}% | {X.XX}% |
| {Region 3} | {X} | {X}% | {X.X}% | {X.XX}% |
| **Total** | **{X}** | **100%** | | **{X.XX}%** |

Source: Segment Note {X}, Page {Y}
Inflation Data: {Source}, as of {Date}
```

---

## Paso 1.5: Crear el directorio de trabajo

```
{COMPANY}_{PERIOD}/
|
+-- source/
|   +-- EEFF.md                    # Financial Statements
|   +-- MDA.md                     # Management Discussion
|   +-- note_reference.md          # Note mapping card
|   +-- geographic_data.md         # Inflation weights
|
+-- analysis/
|   +-- agent1_em_findings.md      # Earnings Manipulation
|   +-- agent2_cf_findings.md      # Cash Flow
|   +-- agent3_km_findings.md      # Key Metrics
|   +-- agent4_aa_findings.md      # Acquisition Accounting
|   +-- owner_earnings_calc.md     # OE calculation
|
+-- output/
    +-- {COMPANY}_Financial_Shenanigans_{PERIOD}.md
    +-- {COMPANY}_Owner_Earnings_{PERIOD}.md
    +-- {COMPANY}_CFO_Questions_{PERIOD}.md
```

---

## Paso 1.6: Lista de verificación previa al lanzamiento

Antes de lanzar los agentes de la Fase 2, verifica:

### Documentos listos
- [ ] Estados financieros en formato Markdown
- [ ] MD&A / Analisis Razonado en formato Markdown
- [ ] Ambos documentos son legibles y están bien formateados

### Mapeo de notas completo
- [ ] Todas las notas esenciales identificadas con sus números de página
- [ ] Ficha de referencia de notas creada
- [ ] Datos clave marcados

### Datos geográficos listos
- [ ] Ponderaciones de ingresos por país calculadas
- [ ] Tasas de inflación locales obtenidas
- [ ] Inflación combinada calculada

### Directorio de trabajo creado
- [ ] Estructura de directorios en su lugar
- [ ] Archivos fuente copiados
- [ ] Listo para las salidas de los agentes

---

## Problemas comunes y soluciones

| Problema | Solución |
|-------|----------|
| Las tablas del PDF se convirtieron mal | Usa la skill pdf para extraer las tablas, o léelas en la imagen de la página y corrígelas a mano |
| Los números de nota son inconsistentes | Crea una correspondencia entre los años fiscales |
| Faltan datos de segmentos | Revisa la MD&A para encontrar la discusión geográfica |
| No hay datos de inflación disponibles | Usa el sitio web del banco central o el Banco Mundial |
| Varias monedas | Convierte a la moneda de presentación usando los tipos de cambio informados |

---

## Ejemplo: preparación de una empresa de telecomunicaciones

```markdown
## ACME Telecom - Q4 2025 Preparation

### Documents Collected
- 10-K filed 2/15/2026 (SEC EDGAR)
- Converted to Markdown: ACME_10K_2025.md

### Note Reference Card
| Category | Note # | Page |
|----------|--------|------|
| Revenue | Note 2 | p.45 |
| Receivables | Note 5 | p.52 |
| PPE | Note 8 | p.58 |
| Intangibles | Note 9 | p.61 |
| Income Taxes | Note 12 | p.68 |
| Segments | Note 18 | p.82 |

### Geographic Data
| Region | Weight | Inflation | Weighted |
|--------|--------|-----------|----------|
| USA | 70% | 3.2% | 2.24% |
| Canada | 20% | 2.8% | 0.56% |
| Mexico | 10% | 4.5% | 0.45% |
| **Blended** | | | **3.25%** |

### Ready for Phase 2: YES
```
