# Owner Earnings - Reglas para Empresas en Decrecimiento

> **Parent Skill**: [SKILL.md](../SKILL.md)

---

## Cuando el Volumen de Negocio DECRECE

**Si la base de clientes, unidades vendidas, o volumen fisico esta cayendo:**

```python
if crec_volumen_pct <= 0:  # Decrecimiento o estancamiento
    # TODO el CAPEX va a mantenimiento, NADA a crecimiento
    capex_crecimiento = 0
    capex_mantenimiento = max(capex_ppe, mc_floor)  # Usar el mayor
```

**Logica**: Si el negocio no crece en volumen, cualquier inversion es solo para mantener lo que ya existe. No hay justificacion para asignar CAPEX a "crecimiento".

## El Castigo por Sub-Inversion en Empresas Decrecientes

Cuando una empresa en decrecimiento tiene sub-inversion, el impacto es DOBLE:
1. **No genera crecimiento** (por definicion, esta decreciendo)
2. **Erosiona capacidad productiva** (no repone activos a costo real)

**Formula para Owner Earnings en este caso:**

```python
# Para empresas en decrecimiento con sub-inversion
if crec_volumen_pct <= 0 and capex_ppe < mc_floor:
    # CASTIGO COMPLETO: Usar suelo de inflacion como costo real
    capex_mantenimiento = mc_floor  # NO el CAPEX real
    owner_earnings = net_income + da + deterioro_ppe - mc_floor

    # Los OE pueden ser NEGATIVOS - esto es correcto!
    # Significa que la empresa DESTRUYE valor
```

## Ejemplo Real: ENTEL 2025 (Empresa Decreciente + Sub-Inversion)

```
DATOS:
- Clientes Chile: -4% (decrecimiento)
- Prepago Chile: -32% (colapso)
- Edad Activos: 15.9 años (Deprec.Acum / Deprec.Anual)
- Inflacion Ponderada Chile/Peru: 3.9%

PASO 1 - SUELO BASE (Ajuste Inflacionario):
Factor Inflacion = (1 + 0.039)^15.9 = 1.84
D&A = M$570,766
Suelo Base = 570,766 × 1.84 = M$1,050,209

PASO 2 - AJUSTE POR VOLUMEN (Capacidad Necesaria):
Clientes Actuales: 20.28M
Clientes Pico Historico: ~22M
Ratio Utilizacion = 20.28 / 22 = 0.922 (92.2%)

Suelo Real = Suelo Base × Ratio
           = 1,050,209 × 0.922 = M$968,293

PASO 3 - DETECCION SUB-INVERSION:
CAPEX Real:          M$   535,317
Suelo Real:          M$   968,293
DEFICIT:             M$  (432,976)  ← 45% sub-inversion!

PASO 4 - OWNER EARNINGS (CONSERVADOR):
Net Income Ajustado:           M$     89,153
+ D&A:                         M$    570,766
+ Deterioro PPE:               M$     14,853
- CAPEX Mant. (SUELO REAL):    M$   (968,293)  ← Ajustado!
─────────────────────────────────────────────────────────
= OWNER EARNINGS:              M$   (293,521)  ← NEGATIVO

INTERPRETACION:
Incluso ajustando por menor utilizacion de capacidad (92%),
la empresa DESTRUYE M$293,521 MM de valor al año. El CAPEX
real de M$535,317 es solo 55% del Suelo Real necesario.
```

## Red Flags de Sub-Inversion Cronica

| Señal | Que Indica |
|-------|------------|
| CAPEX < D&A por 3+ años | Erosion de capacidad productiva |
| CAPEX < 50% del Suelo | Sub-inversion severa, destruccion de valor |
| Edad activos > 15 años | Alto riesgo de obsolescencia |
| OE negativos post-ajuste | Empresa no genera valor real para dueños |
| D&A/Ventas cayendo | Puede indicar activos no renovados |

## Cuando Usar Esta Regla

| Situacion | Aplicar Regla? |
|-----------|---------------|
| Ventas crecen pero clientes caen | SI - volumen fisico cae |
| Ventas crecen por precio, no volumen | SI - crecimiento artificial |
| Empresa madura sin expansion | SI - todo es mantenimiento |
| Industria en declive (ej: prensa escrita) | SI - agresivamente |
| Empresa en turnaround con plan creible | PARCIAL - evaluar caso |
| Startup en hipercrecimiento | NO - usar formula estandar |
