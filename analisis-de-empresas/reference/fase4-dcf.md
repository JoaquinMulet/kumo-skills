# Fase 4: Valoración por DCF usando Owner Earnings

> **Skill padre**: [SKILL.md](../SKILL.md)
> **Filosofía**: "Price is what you pay, value is what you get" (Precio es lo que pagas, valor es lo que recibes). Warren Buffett

---

## Por qué Owner Earnings > FCF estándar para el DCF

Los modelos DCF estándar usan el flujo de caja libre (CFFO - CapEx). Esto tiene dos problemas:
1. No separa el CapEx de mantenimiento del CapEx de crecimiento
2. No ajusta por inflación el costo de reposición de los activos

Los Owner Earnings resuelven ambos:
```
Owner Earnings = Adjusted NI + D&A + Non-Cash - MAINTENANCE CapEx only
```

El CapEx de crecimiento se excluye porque crea valor FUTURO, no actual.

---

## Paso 4.1: Reunir los insumos de las fases anteriores

De la Fase 2 (manipulaciones contables):
- Utilidad neta ajustada (sin partidas no recurrentes)
- Puntaje de calidad de las utilidades (afecta la tasa de descuento)

De la Fase 3 (Owner Earnings):
- Owner Earnings (3 escenarios: pesimista/base/optimista)
- Margen de OE (para la estabilidad de la proyección)
- ROIIC (para los supuestos de retorno de la reinversión)
- Indicador de subinversión (afecta el crecimiento terminal)

De los datos de mercado:
- Precio actual de la acción
- Acciones en circulación (diluidas)
- Capitalización bursátil actual
- Tasa libre de riesgo (Treasury a 10 años)
- Prima de riesgo de mercado
- Beta de la empresa (si se usa CAPM)
- Deuda neta o caja neta

---

## Paso 4.2: Cálculo del WACC

### Costo del patrimonio (enfoque de Buffett vs CAPM)

**CAPM (estándar):**
```
Ke = Rf + Beta × ERP
```

**Enfoque de Buffett (preferido):**
Buffett usa el Treasury a 10 años como tasa mínima exigida, con una prima por calidad:

| Calidad del negocio | Tasa mínima exigida |
|-----------------|-------------|
| Excelente (foso competitivo amplio, ROIC alto) | Treasury a 10 años + 2-3% |
| Buena (foso competitivo estrecho, ROIC decente) | Treasury a 10 años + 4-5% |
| Promedio (sin foso competitivo, ROIC ≈ WACC) | Treasury a 10 años + 6-8% |
| Riesgosa (manipulaciones contables detectadas, frágil) | Treasury a 10 años + 10%+ |

**Ajustes según nuestro análisis:**
- Si el puntaje de manipulaciones contables > 8: sumar +2% a la tasa de descuento
- Si el puntaje de fragilidad > 3.5: sumar +1.5%
- Si el skin in the game de la administración = DÉBIL: sumar +1%

### Costo de la deuda
```
Kd = Interest Expense / Average Total Debt × (1 - Tax Rate)
```

### WACC
```
WACC = (E/V × Ke) + (D/V × Kd)
```

---

## Paso 4.3: Proyectar los Owner Earnings (5-10 años)

### Marco de la tasa de crecimiento

Usa el margen de Owner Earnings × el crecimiento proyectado de los ingresos:

| Año | Crecimiento de ingresos | Margen de OE | Owner Earnings |
|------|---------------|-----------|---------------|
| Año 0 (real) | - | {X}% | M$ {real} |
| Año 1 | {X}% | {X}% | M$ {proyectado} |
| Año 2 | {X}% | {X}% | M$ {proyectado} |
| ... | desvanecimiento gradual | estable o en mejora | ... |
| Año 5/10 | {terminal}% | {normalizado}% | M$ {proyectado} |

### Límites de la tasa de crecimiento (disciplina de Buffett)

| Restricción | Regla |
|-----------|------|
| Tasa máxima de crecimiento | MIN(ROIIC histórico × tasa de reinversión, 15%) |
| Tasa mínima de crecimiento | MAX(tasa de inflación, 0%) para empresas en marcha |
| Tasa de crecimiento terminal | Nunca superar el crecimiento del PIB (2-3% nominal) |
| Reversión a la media | Todas las tasas de crecimiento convergen hacia el promedio de la industria al año 5 |
| Indicador de subinversión | Si la empresa subinvierte, limitar el crecimiento a 0% |

### Proyección del margen de OE

| Escenario | Enfoque |
|----------|----------|
| Negocio estable | Usar el margen de OE promedio de 3 a 5 años |
| Negocio en mejora | Expansión gradual hacia lo mejor de su clase entre los pares |
| Negocio en deterioro | Compresión gradual hacia la mediana de la industria |
| Recuperación (turnaround) | Mostrar un escenario aparte; no suponer mejora en el caso base |

---

## Paso 4.4: Valor terminal

### Dos métodos (verificación cruzada)

**Método 1: Crecimiento a perpetuidad (Gordon)**
```
TV = OE_terminal × (1 + g) / (WACC - g)
```

**Método 2: Múltiplo de salida (de la Fase 5 de comparables)**
```
TV = OE_terminal × Peer_Median_P/OE_multiple
```

### Verificaciones de sensatez del valor terminal
- El TV debe ser 50-70% del valor total del DCF (si es >80%, tu período de crecimiento es demasiado corto)
- El crecimiento terminal implícito debe ser < crecimiento del PIB
- El múltiplo terminal implícito debe ser razonable frente a los pares actuales

---

## Paso 4.5: Calcular el valor intrínseco

```
Enterprise Value = Sum(PV of projected OE) + PV of Terminal Value

Equity Value = Enterprise Value - Net Debt + Excess Cash

Intrinsic Value per Share = Equity Value / Diluted Shares

Margin of Safety = (Intrinsic Value - Current Price) / Intrinsic Value
```

### Tabla de valoración de tres escenarios

| Escenario | OE usado | WACC | Crecimiento terminal | Valor intrínseco | vs Precio | Margen de seguridad |
|----------|---------|------|-----------------|----------------|----------|-----------------|
| Bajista | OE pesimista | WACC + 1% | g - 1% | $X | {+/-X%} | {X%} |
| **Base** | **OE base** | **WACC** | **g** | **$Y** | **{+/-X%}** | **{X%}** |
| Alcista | OE optimista | WACC - 0.5% | g + 0.5% | $Z | {+/-X%} | {X%} |

---

## Paso 4.6: Análisis de sensibilidad

### Tres tablas de sensibilidad

**Tabla 1: WACC vs crecimiento terminal**
(matriz de 5×5 que muestra el valor intrínseco con distintas combinaciones de WACC y g)

**Tabla 2: Margen de OE vs crecimiento de ingresos**
(matriz de 5×5 que muestra el valor intrínseco con distintas combinaciones de margen y crecimiento)

**Tabla 3: Factor de eficiencia vs CapEx de mantenimiento**
(Solo para empresas con factor de eficiencia de owner-earnings)
(matriz de 5×5 que muestra cómo distintos supuestos de eficiencia cambian el valor)

---

## Paso 4.7: Evaluación del margen de seguridad

### Marco de decisión de Buffett

| Margen de seguridad | Calidad exigida | Acción |
|-----------------|-----------------|--------|
| >40% | Cualquier calidad | Compra fuerte (valor profundo) |
| 20-40% | Buena a excelente | Comprar |
| 10-20% | Solo excelente | Considerar (si el foso competitivo es amplio) |
| 0-10% | - | Valor justo, no comprar |
| Negativo | - | Sobrevalorada, considerar vender en corto |

### Integración con el marco de riesgo
- Si el riesgo de pérdida permanente = BAJO → aceptar 20% de margen de seguridad
- Si el riesgo de pérdida permanente = MEDIO → exigir 30%+
- Si el riesgo de pérdida permanente = ALTO → exigir 40%+ o evitar

---

## Formato de salida

```markdown
## DCF Valuation - {COMPANY}

### Key Assumptions
| Parameter | Value | Source |
|-----------|-------|--------|
| WACC | {X}% | Calculated |
| Terminal Growth | {X}% | GDP-anchored |
| Projection Period | {X} years | Standard |
| Base OE | M${X} | Phase 3 |
| OE Growth Rate Y1 | {X}% | {rationale} |

### Valuation Summary
| Scenario | Intrinsic Value | vs Price | Margin of Safety |
|----------|----------------|----------|-----------------|
| Bear | ${X} | {X%} | {X%} |
| Base | ${X} | {X%} | {X%} |
| Bull | ${X} | {X%} | {X%} |

### Verdict
- Current Price: ${X}
- Base Intrinsic Value: ${X}
- Margin of Safety: {X%}
- Required MoS (given risk): {X%}
- **Decision: {BUY / FAIR VALUE / OVERVALUED}**
```
