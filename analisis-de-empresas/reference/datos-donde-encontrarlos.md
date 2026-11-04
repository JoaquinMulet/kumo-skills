# Mapa de ubicación de datos: 10-K vs EEFF

Referencia rápida para encontrar los datos clave en los reportes de EE.UU. (10-K) e internacionales (EEFF).

---

## Datos de Owner Earnings

### Insumos centrales del cálculo

| Dato | 10-K (US GAAP) | EEFF (IFRS/NIIF) |
|------|----------------|------------------|
| **Utilidad neta** | Estado de resultados, última línea | Estado de Resultados, "Ganancia (Perdida)" |
| **Depreciación - PPE** | Flujo de caja (operación) o nota de PPE | Nota 14, "Gasto por Depreciacion" o Estado de Flujos |
| **Depreciación - ROU** | Flujo de caja (operación) o nota de arrendamientos | Nota 28, "Depreciacion Derechos de Uso" |
| **Amortización - Intangibles** | Flujo de caja (operación) o nota de intangibles | Nota 12, o Estado de Resultados |
| **D&A total** | Estado de resultados o flujo de caja | Estado de Resultados, línea "Gasto por Depreciacion y Amortizacion" |
| **CAPEX (PPE)** | Flujo de caja - inversión, "Purchases of PPE" (compras de PPE) | Estado de Flujos, "Compras de Propiedades, Planta y Equipo" |
| **CAPEX (Intangibles)** | Flujo de caja - inversión, "Purchases of Intangibles" (compras de intangibles) | Estado de Flujos, "Compras de Activos Intangibles" |

### Cálculo de la antigüedad de los activos

| Dato | Ubicación en el 10-K | Ubicación en los EEFF |
|------|---------------|---------------|
| **PPE bruto** | Nota de PPE, columna "Cost" (costo) o "Gross" (bruto) | Nota 14, "Costo" o "Valor Bruto" |
| **Depreciación acumulada** | Nota de PPE, línea de contra-activo | Nota 14, "Depreciacion Acumulada" |
| **PPE neto** | Balance o nota de PPE | Estado de Situacion, "Propiedades, Planta y Equipo" |
| **Depreciación anual** | Nota de PPE o flujo de caja | Nota 14 (movimiento) o Estado de Resultados |

**Fórmula**:
```
Asset Age = Accumulated Depreciation / Annual Depreciation
```

### Cálculo de Alpha (intensidad de capital)

| Dato | Ubicación en el 10-K | Ubicación en los EEFF |
|------|---------------|---------------|
| **PPE bruto** | Nota de PPE | Nota 14 |
| **Ingresos** | Estado de resultados, primera línea | Estado de Resultados, "Ingresos de Actividades Ordinarias" |

**Fórmula**:
```
Alpha = Gross PPE / Revenue
```

---

## Datos para detectar manipulaciones contables

### Categoría 1: Manipulación de utilidades (EM)

| Dato | Ubicación en el 10-K | Ubicación en los EEFF | Se usa para |
|------|---------------|---------------|----------|
| **Política de reconocimiento de ingresos** | Nota "Summary of Significant Policies" (resumen de políticas significativas), sección de ingresos | Nota 3, sección "Ingresos" | EM-1, EM-2 |
| **Ingresos diferidos** | Balance (pasivos) o nota de ingresos | Nota 19, "Otros Pasivos No Financieros" | EM-1, EM-6 |
| **Cuentas por cobrar** | Balance + nota de cuentas por cobrar | Nota 8, "Deudores Comerciales" | EM-1, EM-2 |
| **Provisión para cuentas incobrables** | Nota de cuentas por cobrar | Nota 8, "Deterioro" | EM-1 |
| **Ingresos con partes relacionadas** | Nota de partes relacionadas | Nota 9, "Transacciones con Relacionadas" | EM-2 |
| **Otros ingresos y ganancias** | Estado de resultados | Estado de Resultados, "Otros Ingresos" | EM-3 |
| **Ganancia por venta de activos** | Estado de resultados o flujo de caja | Estado de Flujos (inversión) u otros ingresos | EM-3 |
| **Activo por impuesto diferido** | Nota de impuestos a las ganancias | Nota 15, "Activos por Impuestos Diferidos" | EM-3 |
| **Costos capitalizados** | Nota de PPE, nota de intangibles | Nota 14, Nota 12 | EM-4 |
| **Vidas útiles** | Nota de PPE, política de depreciación | Nota 3, "Depreciacion" | EM-4 |
| **Pasivos contingentes** | Nota de compromisos | Nota 32, "Contingencias" | EM-5 |
| **Reservas de reestructuración** | Nota de reestructuración | Nota 18, "Provisiones" | EM-7 |

### Categoría 2: Manipulaciones del flujo de caja (CF)

| Dato | Ubicación en el 10-K | Ubicación en los EEFF | Se usa para |
|------|---------------|---------------|----------|
| **CFFO** | Estado de flujo de caja - operación | Estado de Flujos, "Actividades de Operacion" | Todos los CF |
| **CFI** | Estado de flujo de caja - inversión | Estado de Flujos, "Actividades de Inversion" | CF-1, CF-2 |
| **CFF** | Estado de flujo de caja - financiamiento | Estado de Flujos, "Actividades de Financiacion" | CF-1, CF-2 |
| **Variación en cuentas por cobrar** | Flujo de caja (operación) | Estado de Flujos, dentro de operación | CF-3 |
| **Variación en cuentas por pagar** | Flujo de caja (operación) | Estado de Flujos, dentro de operación | CF-3 |
| **Variación en inventarios** | Flujo de caja (operación) | Estado de Flujos, dentro de operación | CF-3 |
| **Factoring de cuentas por cobrar** | Nota de deuda o nota de cuentas por cobrar | Nota 8 o Nota 16 | CF-1 |

### Categoría 3: Métricas clave (KM)

| Dato | Ubicación en el 10-K | Ubicación en los EEFF | Se usa para |
|------|---------------|---------------|----------|
| **Ingresos por segmento** | Nota de segmentos | Nota 29, "Informacion por Segmentos" | KM-1, KM-2 |
| **Utilidad por segmento** | Nota de segmentos | Nota 29 | KM-1 |
| **Conciliación non-GAAP** | MD&A o comunicado de resultados | Analisis Razonado | KM-1 |
| **EBITDA** | MD&A (normalmente) | Analisis Razonado | KM-1 |
| **EPS ajustado** | MD&A o comunicado de resultados | Analisis Razonado | KM-1 |
| **KPI (suscriptores, etc.)** | MD&A | Analisis Razonado | KM-1 |

### Categoría 4: Contabilidad de adquisiciones (AA)

| Dato | Ubicación en el 10-K | Ubicación en los EEFF | Se usa para |
|------|---------------|---------------|----------|
| **Combinaciones de negocios** | Nota "Acquisitions" (adquisiciones) o "Business Combinations" (combinaciones de negocios) | Nota sobre Combinaciones de Negocios | AA-1 |
| **Goodwill** | Balance + nota de goodwill | Nota 13, "Plusvalia" | AA-1, AA-2 |
| **Intangibles adquiridos** | Nota de intangibles | Nota 12, "Activos Intangibles" | AA-1 |
| **Asignación del precio de compra** | Nota de adquisiciones | Nota sobre Combinaciones | AA-1 |
| **DTA por entidad** | Nota de impuestos a las ganancias | Nota 15, desglose por filial | AA-2 |
| **Provisión de valuación** | Nota de impuestos a las ganancias | Nota 15, "Provision por Valuacion" | AA-2 |
| **Prueba de deterioro** | Nota de goodwill | Nota 13, "Deterioro" | AA-2 |

---

## Datos geográficos y de inflación

| Dato | Ubicación en el 10-K | Ubicación en los EEFF |
|------|---------------|---------------|
| **Ingresos por zona geográfica** | Nota de segmentos | Nota 29 |
| **Activos por zona geográfica** | Nota de segmentos | Nota 29 |
| **Ubicación de las filiales** | Nota 1 o nota de filiales | Nota 1, "Informacion Corporativa" |
| **Moneda funcional** | Nota 2 (políticas) | Nota 2 o Nota 3 |
| **Tipos de cambio usados** | Nota de moneda extranjera | Nota 27, "Diferencias de Cambio" |

**Para las tasas de inflación**: usa fuentes externas:
- EE.UU.: Bureau of Labor Statistics (Oficina de Estadísticas Laborales, índice de precios al consumidor)
- Chile: Instituto Nacional de Estadisticas (IPC)
- Perú: INEI
- Europa: Eurostat
- General: World Bank (Banco Mundial), IMF (Fondo Monetario Internacional)

---

## Fórmulas rápidas con referencias a las fuentes

### Antigüedad de los activos

```
Asset Age = Accumulated Depreciation / Annual Depreciation

10-K Sources:
- Accumulated Depr: PPE Note, "Accumulated Depreciation" line
- Annual Depr: Cash Flow Statement, "Depreciation" or PPE Note roll-forward

EEFF Sources:
- Accumulated Depr: Nota 14, "Depreciacion Acumulada" column
- Annual Depr: Nota 14 movement table, or Estado de Resultados D&A line

Example:
Accumulated Depr (Note 14): M$6,628,459
Annual Depr (Note 14): M$417,642
Asset Age: 15.9 years
```

### Alpha (intensidad de capital)

```
Alpha = Gross PPE / Revenue

10-K Sources:
- Gross PPE: PPE Note, "Cost" or first column before depreciation
- Revenue: Income Statement, first line

EEFF Sources:
- Gross PPE: Nota 14, "Costo" column, total row
- Revenue: Estado de Resultados, "Ingresos de Actividades Ordinarias"

Example:
Gross PPE (Note 14): M$8,709,766
Revenue (Income Statement): M$2,954,930
Alpha: 2.95x
```

### Piso de inflación (efecto Reina Roja)

```
Floor = D&A × (1 + inflation)^asset_age × utilization_ratio

Sources:
- D&A: Income Statement or Cash Flow
- Inflation: Weighted average from Segment Note + external sources
- Asset Age: Calculated above
- Utilization: Current volume / Peak volume (from MD&A KPIs)

Example:
D&A: M$570,766
Inflation: 3.9% (weighted Chile 60% + Peru 40%)
Asset Age: 15.9 years
Factor: (1.039)^15.9 = 1.84
Utilization: 92.2% (20.28M / 22M subscribers)

Floor = 570,766 × 1.84 × 0.922 = M$968,293
```

### CAPEX de mantenimiento (regla MAX)

```
Maintenance CAPEX = MAX(Alpha Method, Inflation Floor)

Alpha Method:
- If volume growing: CAPEX - (Alpha × ΔVolume Revenue)
- If volume declining: All CAPEX = Maintenance

Inflation Floor:
- Calculated above

Example:
Alpha Method: M$535,317 (all CAPEX, volume declining)
Inflation Floor: M$968,293

MAX(535,317, 968,293) = M$968,293
```

### Owner Earnings

```
OE = Adjusted Net Income + D&A + Non-Cash Items - Maintenance CAPEX

Sources:
- Adjusted NI: Income Statement - shenanigans adjustments
- D&A: Income Statement or Cash Flow
- Non-Cash: Impairments, restructuring from Notes
- Maint CAPEX: MAX rule result above

Example:
Adjusted NI: M$89,153
D&A: M$570,766
Impairment PPE: M$14,853
Maint CAPEX: M$968,293

OE = 89,153 + 570,766 + 14,853 - 968,293 = M$(293,521)
```

---

## Errores comunes

| Problema | Solución |
|-------|----------|
| La D&A está repartida en varias líneas | Suma toda la depreciación y amortización del estado de resultados |
| La nota de PPE muestra solo el valor neto | Busca las columnas "Cost" (costo) y "Accumulated" (acumulada), o usa el año anterior + adiciones - bajas |
| El CAPEX incluye adquisiciones | Separa "Purchases of PPE" (compras de PPE) de "Business Acquisitions" (adquisiciones de negocios) en el flujo de caja |
| Varias monedas | Usa la moneda de presentación; revisa los ajustes por tipo de cambio en las notas |
| Datos de segmentos incompletos | Complementa con la discusión geográfica del MD&A |
| Datos de inflación desactualizados | Usa el IPC de los últimos 12 meses más reciente del banco central |
