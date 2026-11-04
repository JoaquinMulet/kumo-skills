
# Owner Earnings - Framework Completo de Calculo

Framework para calcular las **Owner Earnings** (Ganancias del Dueno) de Warren Buffett, con ajustes por inflacion del framework Greenwald y validacion de calidad de ganancias de Richardson.

## Concepto Fundamental

**Owner Earnings** = Efectivo real que el dueno puede extraer del negocio sin danar su capacidad productiva.

```
Owner Earnings = Utilidad Neta + D&A - CAPEX Mantenimiento
```

La diferencia clave con Free Cash Flow tradicional es la **separacion precisa de CAPEX** entre:
- **Mantenimiento**: Lo minimo para mantener la capacidad actual
- **Crecimiento**: Inversion discrecional en nueva capacidad

---

## Flujo de Calculo Completo

```
PASO 1: Datos Base
    |
    v
PASO 2: Calcular Alpha (Intensidad Capital)
    |
    v
PASO 3: Separar Crecimiento Volumen vs Precio (MD&A)
    |
    v
PASO 4: Calcular Edad de Activos
    |
    v
PASO 5: Calcular Suelo de Inflacion (Efecto Reina Roja)
    |
    v
PASO 5.5: Factor de Eficiencia Tecnologica [OPCIONAL]
    |      (Solo si empresa en transicion de modelo/tecnologia)
    v
PASO 6: Determinar CAPEX de Crecimiento Organico
    |
    v
PASO 7: Separar CAPEX Mantenimiento vs Crecimiento
    |
    v
PASO 8: Ajustes No Monetarios + Owner Earnings
    |
    v
PASO 9: Metricas Complementarias (ROIIC, Richardson)
```

---

## PASO 1: Datos Base Requeridos

### Del Estado de Resultados
| Campo | Descripcion |
|-------|-------------|
| `ventas` | Net Sales / Revenue |
| `utilidad_neta` | Net Income |
| `utilidad_operativa` | Operating Income / EBIT |
| `depreciacion` | Depreciation Expense |
| `amortizacion` | Amortization Expense |

### Del Balance General
| Campo | Descripcion |
|-------|-------------|
| `ppe_bruto` | Property, Plant & Equipment (Gross) |
| `depreciacion_acumulada` | Accumulated Depreciation |
| `inventarios` | Inventories |
| `cuentas_pagar` | Accounts Payable |

### Del Cash Flow Statement
| Campo | Descripcion |
|-------|-------------|
| `capex_ppe` | Purchases of PP&E |
| `adquisiciones` | Acquisitions / Business Combinations |

### Del MD&A
| Campo | Descripcion |
|-------|-------------|
| `crec_ventas_base_pct` | Crecimiento "Base Business" (excluye M&A) |
| `impacto_precio_pct` | Impacto de inflacion/precio en ventas |
| `inflacion_pct` | CPI anual del pais |

---

## PASO 2: Alpha - Intensidad de Capital

```python
alpha = ppe_bruto / ventas
alpha_5y = alpha.rolling(window=5, min_periods=3).mean()
```

| Alpha | Tipo de Negocio |
|-------|-----------------|
| < 0.05 | Asset-light (Software, Servicios) |
| 0.05 - 0.15 | Moderado (Distribucion, Retail) |
| 0.15 - 0.30 | Capital-intensive (Manufactura) |
| > 0.30 | Heavy-capital (Utilities, Petroleo) |

---

## PASO 3: Separar Volumen vs Precio

```python
crec_volumen_pct = crec_ventas_base_pct - impacto_precio_pct
delta_ventas_volumen = ventas_anterior * (crec_volumen_pct / 100)
```

- **Volumen positivo**: Requiere CAPEX de crecimiento
- **Volumen negativo o cero**: TODO el CAPEX va a mantenimiento

---

## PASO 4: Calcular Edad de Activos

```python
edad_activos = depreciacion_acumulada / depreciacion_anual
```

---

## PASO 5: Suelo de Inflacion (Efecto Reina Roja)

La depreciacion contable subestima el costo REAL de reponer activos porque ignora la inflacion.

```python
factor_inflacion = (1 + inflacion_promedio) ** edad_activos
mc_floor = depreciacion * factor_inflacion
```

---

## PASO 5.5: Factor de Eficiencia Tecnologica [OPCIONAL]

Aplica SOLO cuando hay evidencia clara de transicion tecnologica (ej: telco 4G→5G, banca→digital). Reduce el Suelo de Inflacion por eficiencias demostradas en MD&A. Factor maximo: 0.50 (50% reduccion). Requiere validacion por resultados (servicio no deteriorado).

```python
suelo_ajustado = mc_floor * factor_eficiencia  # factor entre 0.50 y 1.00
```

> Detalle completo: [references/efficiency-factor.md](oe-factor-de-eficiencia.md)

---

## PASO 6: CAPEX de Crecimiento Organico

```python
if crec_volumen_pct > 0:
    capex_crecimiento_organico = alpha_5y * delta_ventas_volumen
else:
    capex_crecimiento_organico = 0  # Todo va a mantenimiento
```

---

## PASO 7: Separacion Final de CAPEX

### REGLA FUNDAMENTAL: USAR EL MAXIMO

```
CAPEX Mantenimiento = MAX(Metodo Alpha, Piso de Inflacion)
```

```python
capex_mantenimiento_final = max(
    capex_mantenimiento_alpha,  # CAPEX Total - CAPEX Crecimiento (si hay)
    mc_floor                     # D&A x (1+inflacion)^edad
)
```

### Deteccion de Sub-Inversion

```python
sub_inversion = mc_floor > capex_ppe

if sub_inversion:
    capex_disponible_crecimiento = 0
    capex_mantenimiento = mc_floor  # Usar SUELO como costo real
else:
    capex_disponible_crecimiento = capex_ppe - mc_floor
    capex_crecimiento_organico_efectivo = min(capex_crecimiento_organico, capex_disponible_crecimiento)
    capex_mantenimiento = capex_ppe - capex_crecimiento_organico_efectivo

capex_crecimiento_total = capex_crecimiento_organico_efectivo + adquisiciones
```

### Empresas en Decrecimiento

Si volumen cae, TODO el CAPEX es mantenimiento. Si ademas hay sub-inversion, usar el Suelo como costo real. Los OE pueden ser NEGATIVOS (empresa destruye valor).

> Detalle completo con ejemplo ENTEL: [references/declining-business-rules.md](oe-negocios-en-declive.md)

---

## PASO 8: Ajustes No Monetarios + Owner Earnings

### Resumen de Ajustes

| Accion | Partidas |
|--------|----------|
| **SUMAR** (no salieron en efectivo) | D&A, SBC, Amort. Intangibles M&A, Impuestos Diferidos (incr.), Impairments, Reestructuracion, Perdidas No Realizadas |
| **RESTAR** (no entraron en efectivo) | Ganancias No Realizadas, Impuestos Diferidos (decr.), Ganancia Venta Activos |
| **RESTAR** (uso de efectivo) | CAPEX Mantenimiento (PASO 7) |

**SBC**: Si > 5% de Utilidad Neta, usar enfoque conservador (no sumar). Critico en tech.

> Detalle completo con ejemplos y ubicaciones en 10-K: [references/non-cash-adjustments.md](oe-ajustes-sin-caja.md)

---

## PASO 9: Owner Earnings Finales

```python
owner_earnings = utilidad_neta + ajustes_sumar - ajustes_restar
owner_earnings_margin = owner_earnings / ventas * 100
```

---

## Metricas Complementarias

### ROIIC (Return on Incremental Invested Capital)

```python
nopat = utilidad_operativa * (1 - tasa_impositiva)
nopat_incremental = nopat_3y_sum - nopat_3y_sum.shift(3)
roiic = nopat_incremental / capex_crec_3y_lag * 100
```

| ROIIC | Evaluacion |
|-------|------------|
| > 20% | Excelente asignacion de capital |
| 10-20% | Bueno (supera costo de capital) |
| < 10% | Pobre (destruye valor) |

### Ratio Validacion Proveedores (Richardson)

```python
ratio_validacion = delta_cuentas_pagar / delta_inventarios
```

| Ratio | Significado |
|-------|-------------|
| > 1.0 | Proveedores financian >100% del inventario (excelente) |
| 0.5-1.0 | Normal, proveedores confian |
| < 0.5 | Alerta: proveedores cortan credito |

---

## Banderas Rojas (Red Flags)

### CAPEX
| Señal | Que Indica |
|-------|------------|
| CAPEX PPE < Suelo por 2+ años | Sub-inversion persistente |
| Volumen cae + CAPEX sube | Investigar ineficiencia |
| Edad activos creciente | Activos sin renovacion |

### Calidad de Ganancias
| Partida | % de Util. Neta | Evaluacion |
|---------|-----------------|------------|
| SBC | < 5% | Normal |
| SBC | 5-15% | Ajustar por dilucion |
| SBC | > 15% | Usar como gasto, no sumar |
| Impairments | < 2% | Ignorar si one-time |
| Impairments | > 5% recurrente | Red flag serio |
| Reestructuracion | Anual | Problema estructural |

### Metricas Finales
| Señal | Que Indica |
|-------|------------|
| OE Margin cayendo | Perdida de eficiencia operativa |
| ROIIC < WACC | Cada dolar nuevo destruye valor |
| Ratio Proveedores < 0.5 | Proveedores retiran credito |
| OE >> FCF reportado | Ajustes faltantes, investigar |

---

## Uso para Valoracion DCF

```python
ventas_proyectadas = ventas_actual * (1 + growth_rate) ** anos
oe_proyectados = ventas_proyectadas * oe_margin_promedio
valor_presente = oe_proyectados / ((1 + discount_rate) ** anos)
precio_intrinseco = sum(valor_presente) / acciones_outstanding
```

---

## Referencias

### Documentos de Referencia (Detalle)
- [Factor de Eficiencia Tecnologica (PASO 5.5)](oe-factor-de-eficiencia.md)
- [Ajustes de Partidas No Monetarias (PASO 8)](oe-ajustes-sin-caja.md)
- [Reglas para Empresas en Decrecimiento](oe-negocios-en-declive.md)
- [Template de Codigo Python](oe-plantilla-python.md)
- [Ejemplo Completo: Pool Corp](oe-ejemplo-pool-corp.md)

### Fuentes Academicas
- **Greenwald, Bruce**: "Value Investing: From Graham to Buffett and Beyond"
- **Buffett, Warren**: Berkshire Hathaway Letters (Owner Earnings definition)
- **Richardson et al. (2004)**: "The Information Content of Accruals"
- **10-K Filings**: SEC EDGAR para datos de empresas publicas USA
