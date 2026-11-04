# Owner Earnings - Ajustes de Partidas No Monetarias (PASO 8)

> **Parent Skill**: [SKILL.md](../SKILL.md)

---

**Concepto Critico**: La Utilidad Neta contiene partidas que NO representan flujo de efectivo real. Debemos identificarlas y ajustarlas para obtener los Owner Earnings verdaderos.

## Formula Completa con Todos los Ajustes

```
Owner Earnings = Utilidad Neta
                + Depreciacion & Amortizacion (D&A)
                + Stock-Based Compensation (SBC)
                + Amortizacion de Intangibles de Adquisicion
                + Impuestos Diferidos (cambio neto)
                + Deterioros (Impairments) no recurrentes
                + Cargos de Reestructuracion no recurrentes
                + Perdidas No Realizadas (mark-to-market)
                - Ganancias No Realizadas (mark-to-market)
                - CAPEX de Mantenimiento
                +/- Cambio en Working Capital Operativo (opcional)
```

## 8.1 Partidas a SUMAR (No salieron en efectivo)

| Partida | Donde Encontrarla | Por Que Ajustar |
|---------|-------------------|-----------------|
| **Depreciacion** | Cash Flow Statement - Operating | Gasto contable, no salio efectivo |
| **Amortizacion** | Cash Flow Statement - Operating | Gasto contable de intangibles |
| **Stock-Based Compensation (SBC)** | Cash Flow Statement - Operating o Nota de Equity | Gasto de compensacion en acciones, no efectivo. CRITICO en tech |
| **Amortizacion Intangibles Adquisicion** | Notas - Intangible Assets | Customer relationships, trade names de M&A. No es costo operativo real |
| **Impuestos Diferidos (incremento)** | Cash Flow Statement - Operating | Si aumenta DTA o disminuye DTL, se registro gasto que no se pago |
| **Deterioros (Impairments)** | Income Statement - Other o Notas | Write-downs de goodwill, PPE, inventario. No recurrente, no efectivo |
| **Cargos Reestructuracion** | Income Statement o Notas | Severance, cierre plantas. No recurrente |
| **Perdidas No Realizadas** | Income Statement - Other Income | Mark-to-market de inversiones, derivados. No salio efectivo |

## 8.2 Partidas a RESTAR (Entraron sin ser efectivo real)

| Partida | Donde Encontrarla | Por Que Ajustar |
|---------|-------------------|-----------------|
| **Ganancias No Realizadas** | Income Statement - Other Income | Mark-to-market que infla utilidad sin generar caja |
| **Impuestos Diferidos (disminucion)** | Cash Flow Statement - Operating | Si disminuye DTA o aumenta DTL, se pago menos de lo registrado |
| **Ganancia Venta Activos** | Cash Flow Statement - Investing | Ya esta en CFI, no es operativo recurrente |
| **Ingreso por Pension (si aplica)** | Notas - Pension | Credito contable por retorno esperado > real |

## 8.3 CAPEX de Mantenimiento (RESTAR)

Ya calculado en PASO 7. Es el unico "uso de efectivo" que restamos.

## 8.4 Cambio en Working Capital (OPCIONAL)

**Debate**: Buffett originalmente NO ajustaba por WC, pero para negocios con WC volatil puede ser util.

```python
# Solo si el negocio tiene WC muy variable
delta_wc = (delta_cuentas_cobrar + delta_inventarios) - delta_cuentas_pagar

# Si delta_wc > 0: Se "invirtio" en WC, restar
# Si delta_wc < 0: Se "libero" WC, sumar
```

**Recomendacion**: Para empresas estables, ignorar WC. Para retailers/distribuidores con inventario ciclico, considerar promedio 3-5 anos.

---

## Ejemplo Completo de Ajustes (Empresa Tech Hipotetica)

```
Utilidad Neta Reportada:          $500,000
+ Depreciacion:                   + 50,000
+ Amortizacion:                   + 30,000
+ Stock-Based Compensation:       + 80,000  <- Critico en tech!
+ Amort. Intangibles M&A:         + 25,000
+ Impuestos Diferidos (incr.):    + 15,000
+ Cargo Reestructuracion:         + 10,000  <- One-time
- Ganancia Venta Activo:          - 5,000
- CAPEX Mantenimiento:            - 60,000
----------------------------------------
Owner Earnings Ajustados:         $645,000

vs Utilidad Neta:                 $500,000
Diferencia:                       +29% mayor
```

## Donde Encontrar Cada Partida en el 10-K

| Partida | Ubicacion en 10-K |
|---------|-------------------|
| D&A | Cash Flow Statement, linea "Depreciation and amortization" |
| SBC | Cash Flow Statement, linea "Stock-based compensation" O Nota de Stockholders' Equity |
| Intangibles M&A | Nota "Intangible Assets" - ver amortization expense desglosada |
| Impuestos Diferidos | Cash Flow Statement O Nota "Income Taxes" - reconciliacion |
| Impairments | Income Statement - "Impairment charges" o Nota "Goodwill" |
| Reestructuracion | Nota "Restructuring" o en Operating Expenses con detalle |
| Mark-to-Market | "Other Income/Expense" o Nota "Fair Value Measurements" |

---

## Caso Especial: Stock-Based Compensation (SBC)

**Por que es critico ajustar SBC**:

1. **Es compensacion REAL** a empleados (aunque no en efectivo)
2. **Diluye** a los accionistas existentes
3. En empresas tech puede ser 10-30% de la utilidad neta

**Dos filosofias**:

| Enfoque | Tratamiento | Cuando Usar |
|---------|-------------|-------------|
| **Conservador** | NO sumar SBC (dejarlo como gasto) | Empresas tech con alta dilucion |
| **Buffett Clasico** | Sumar SBC (es no-cash) | Empresas tradicionales con SBC minimo |

**Recomendacion**: Si SBC > 5% de Utilidad Neta, usar enfoque conservador o ajustar por dilucion esperada.

```python
# Enfoque hibrido: Ajustar por dilucion real
sbc_ajustado = sbc * (1 - tasa_dilucion_anual)
# Solo sumar la porcion que NO diluye
```
