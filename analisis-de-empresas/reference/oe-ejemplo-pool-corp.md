# Ejemplo Completo: Pool Corporation 2015-2024

Este documento muestra el calculo paso a paso de Owner Earnings usando datos reales de Pool Corporation.

## Datos Historicos Calculados

| Ano | Ventas | Util. Neta | D&A | CAPEX PPE | Adq. | Suelo | CAPEX Mant. | CAPEX Crec. | Owner Earnings | OE Margin |
|-----|--------|------------|-----|-----------|------|-------|-------------|-------------|----------------|-----------|
| 2015 | 2,363M | 128M | 17K | 29K | 4K | 19K | 29K | 4K | 117K | 4.9% |
| 2016 | 2,571M | 149M | 22K | 34K | 20K | 24K | 34K | 20K | 136K | 5.3% |
| 2017 | 2,788M | 191M | 26K | 39K | 13K | 28K | 28K | 24K | 189K | 6.8% |
| 2018 | 2,998M | 234M | 28K | 32K | 3K | 30K | 30K | 4K | 232K | 7.7% |
| 2019 | 3,200M | 262M | 29K | 33K | 125K | 33K | 33K | 125K | 258K | 8.1% |
| 2020 | 3,937M | 367M | 29K | 22K | 9K | 33K | 33K | 9K | 363K | 9.2% |
| 2021 | 5,296M | 651M | 30K | 38K | 812K | 34K | 34K | 815K | 646K | 12.2% |
| 2022 | 6,180M | 748M | 39K | 44K | 9K | 37K | 37K | 16K | 750K | 12.1% |
| 2023 | 5,542M | 523M | 40K | 60K | 12K | 39K | 60K | 12K | 503K | 9.1% |
| 2024 | 5,311M | 434M | 45K | 59K | 5K | 45K | 59K | 5K | 420K | 7.9% |

*Nota: Valores en miles de USD (K) y millones (M)*

---

## Caso 1: Ano Normal (2024)

### Datos de Entrada
```
ventas = $5,310,953K
utilidad_neta = $434,325K
depreciacion = $36,784K
amortizacion = $8,697K
ppe_bruto = $506,478K
depreciacion_acumulada = $255,154K
capex_ppe = $59,476K
adquisiciones = $4,692K
crec_volumen_pct = -5.5%  (contraccion)
```

### Paso 2: Alpha
```
alpha = 506,478 / 5,310,953 = 0.0954
alpha_5y = 0.0912 (promedio ultimos 5 anos)
```

### Paso 4: Edad de Activos
```
edad = 255,154 / 36,784 = 6.94 anos
```

### Paso 5: Suelo de Inflacion
```
inflacion_promedio = 2.9%
factor = (1.029)^6.94 = 1.217
suelo = 36,784 * 1.217 = $44,779K
```

### Paso 6: CAPEX Crecimiento
```
crec_volumen_pct = -5.5% (NEGATIVO)
capex_crecimiento_organico = 0  # No hay crecimiento de volumen
```

### Paso 7: Separacion CAPEX
```
sub_inversion = 44,779 > 59,476? = NO

capex_disponible = 59,476 - 44,779 = $14,697K
capex_crec_efectivo = min(0, 14,697) = 0

capex_mantenimiento = 59,476 - 0 = $59,476K
capex_crec_total = 0 + 4,692 = $4,692K
```

### Paso 8: Owner Earnings
```
D&A = 36,784 + 8,697 = $45,481K
OE = 434,325 + 45,481 - 59,476 = $420,330K
OE_margin = 420,330 / 5,310,953 = 7.91%
```

---

## Caso 2: Sub-Inversion (2020 - COVID)

### Datos de Entrada
```
ventas = $3,936,623K
utilidad_neta = $366,738K
depreciacion = $27,967K
amortizacion = $1,431K
depreciacion_acumulada = $170,026K
capex_ppe = $21,702K  # Reducido por COVID
adquisiciones = $8,901K
crec_volumen_pct = +18.5%  # Boom COVID
```

### Paso 4-5: Suelo
```
edad = 170,026 / 27,967 = 6.08 anos
factor = (1.029)^6.08 = 1.188
suelo = 27,967 * 1.188 = $33,228K
```

### Paso 7: Deteccion de Sub-Inversion
```
sub_inversion = 33,228 > 21,702? = SI!

deficit = 33,228 - 21,702 = $11,526K
capex_disponible = 0  # Nada disponible para crecimiento
capex_crec_efectivo = 0

# IMPORTANTE: Usamos SUELO como costo real
capex_mantenimiento = $33,228K (no los $21,702K reales)
```

### Paso 8: Owner Earnings (Conservador)
```
D&A = 27,967 + 1,431 = $29,398K
OE = 366,738 + 29,398 - 33,228 = $362,908K
OE_margin = 9.22%
```

**Interpretacion**: Aunque la empresa reporto CAPEX de solo $21,702K,
el costo REAL de mantener los activos era $33,228K. Usamos el suelo
para ser conservadores y reflejar la realidad economica.

---

## Caso 3: Crecimiento Fuerte (2021 - Boom)

### Datos de Entrada
```
ventas = $5,295,584K
ventas_anterior = $3,936,623K
utilidad_neta = $650,624K
crec_volumen_pct = +21.5%
capex_ppe = $37,658K
adquisiciones = $811,956K  # Mega-adquisicion
alpha_5y = 0.075
```

### Paso 3: Delta Ventas Volumen
```
delta_ventas_vol = 3,936,623 * (21.5/100) = $846,374K
```

### Paso 6: CAPEX Crecimiento Organico
```
capex_crec_org = 0.075 * 846,374 = $63,478K
```

### Paso 5: Suelo
```
suelo = $34,264K
```

### Paso 7: Separacion
```
sub_inversion = 34,264 > 37,658? = NO

capex_disponible = 37,658 - 34,264 = $3,394K
capex_crec_efectivo = min(63,478, 3,394) = $3,394K

# El CAPEX PPE no alcanza para todo el crecimiento teorico
# Solo $3,394K va a crecimiento organico

capex_mantenimiento = 37,658 - 3,394 = $34,264K
capex_crec_total = 3,394 + 811,956 = $815,350K
```

**Nota**: La mega-adquisicion de $812M domina el crecimiento este ano.
El ROIIC posterior mostrara si fue buena asignacion de capital.

---

## ROIIC Calculado

| Ano | NOPAT Incr. (3Y) | CAPEX Crec. Lag (3Y) | ROIIC |
|-----|------------------|----------------------|-------|
| 2020 | $429M | $158M | 272% |
| 2021 | $697M | $136M | 512% |
| 2022 | $887M | $780M | 114% |
| 2023 | $825M | $632M | 130% |
| 2024 | $591M | $987M | 60% |

**Interpretacion**:
- 2020-2021: ROIIC extraordinario por boom COVID (demanda > capacidad)
- 2022-2023: Normalizacion pero aun excelente (>100%)
- 2024: Cae a 60% por contraccion de mercado, pero aun supera WACC (~10%)

---

## Diagnostico de Salud del Negocio

### Indicadores Positivos
1. OE Margin promedio 8.2% - Saludable y consistente
2. ROIIC promedio muy superior a WACC
3. Sin sub-inversion cronica (solo 2020 por COVID)
4. Alpha baja (0.08) - Negocio asset-light

### Banderas de Atencion
1. Volumen negativo 2023-2024 (normalizacion post-COVID)
2. Adquisicion grande 2021 - Monitorear integracion
3. Edad de activos estable (~7 anos) - Renovacion adecuada

### Conclusion
Pool Corporation demuestra excelente asignacion de capital con 
Owner Earnings reales y sostenibles. La contraccion reciente es 
normalizacion, no deterioro estructural.
