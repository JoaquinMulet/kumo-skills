# Fase 5: Análisis de comparables con ajuste por calidad

> **Skill padre**: [SKILL.md](../SKILL.md)
> **Idea clave**: una empresa con utilidades limpias merece un múltiplo con prima frente a una con manipulaciones contables

---

## Por qué comparables ajustados por calidad

Los comparables estándar comparan P/E y EV/EBITDA entre pares. Pero estos múltiplos suponen que todas las utilidades son iguales. Nuestro marco sabe que NO lo son:
- Una empresa con 0 hallazgos de manipulaciones contables tiene utilidades más confiables
- Una empresa con Owner Earnings >> utilidades reportadas está subvalorada en las métricas estándar
- Una empresa con Owner Earnings << utilidades reportadas está sobrevalorada en las métricas estándar

---

## Paso 5.1: Seleccionar el grupo de pares

### Criterios de selección (la pregunta de Buffett: "¿compararía yo estos negocios?")
- Modelo de negocio similar (no solo el mismo código SIC)
- Posición competitiva similar (líder de mercado vs retador)
- Intensidad de capital similar (Alpha dentro de 2x del objetivo)
- Exposición geográfica similar
- 5-10 pares como máximo (calidad por sobre cantidad)

### Niveles de calidad de los pares
Si tienes datos de manipulaciones contables de los pares (de análisis anteriores), clasifícalos en niveles:

| Nivel | Criterio | Tratamiento del múltiplo |
|------|----------|-------------------|
| A - Limpia | Puntaje de manipulaciones contables 0-3, OE ≈ utilidades reportadas | Usar el múltiplo completo |
| B - Mixta | Puntaje de manipulaciones contables 4-7, se necesitan algunos ajustes | Aplicar un descuento de 10-15% al múltiplo |
| C - Sospechosa | Puntaje de manipulaciones contables 8+, OE << reportadas | Aplicar un descuento de 20-30% o excluir |

---

## Paso 5.2: Reunir las métricas de los pares

### Métricas operativas centrales
| Métrica | Propósito |
|--------|---------|
| Ingresos | Comparación de escala |
| Crecimiento de ingresos (interanual) | Trayectoria de crecimiento |
| Margen bruto | Poder de fijación de precios / estructura de costos |
| Margen EBITDA | Eficiencia operativa |
| Margen de Owner Earnings* | Generación real de caja (si se puede calcular) |
| ROIC | Retorno sobre el capital invertido |
| Deuda/EBITDA | Comparación de apalancamiento |

*Si no se pueden calcular los Owner Earnings de los pares, usa el margen de FCF como aproximación, con una nota.

### Múltiplos de valoración
| Múltiplo | Cuándo usarlo |
|----------|------------|
| P/E | Empresas rentables, utilidades estables |
| EV/EBITDA | Intensivas en capital, estructuras de capital distintas |
| P/Owner Earnings* | Nuestro preferido, solo si los OE de los pares son calculables |
| EV/Ingresos | Empresas de alto crecimiento o sin utilidades |
| P/Libro | Intensivas en activos, servicios financieros |
| Rendimiento de FCF | Negocios maduros y generadores de caja |

### Bloque de estadísticas
Para cada métrica: Máximo, percentil 75, mediana, percentil 25, mínimo

---

## Paso 5.3: Múltiplo ajustado por calidad

### La fórmula de ajuste

```
Adjusted Multiple = Peer Median Multiple × Quality Premium/Discount

Quality Factor = f(Shenanigans Score, OE/Reported Earnings Ratio, Moat Width)
```

### Cálculo del factor de calidad

| Componente | Ponderación | Rango de puntaje | Cómo calcularlo |
|-----------|--------|-------------|-----------------|
| Confiabilidad de las utilidades | 40% | 0.7 - 1.3 | Razón OE / UN reportada (>1 = confiable, <1 = inflada) |
| Riesgo de manipulaciones contables | 30% | 0.7 - 1.2 | Inverso de la severidad (limpia = 1.2, crítica = 0.7) |
| Amplitud del foso competitivo | 20% | 0.8 - 1.2 | Amplio = 1.2, Estrecho = 1.0, Ninguno = 0.8 |
| Calidad de la administración | 10% | 0.8 - 1.2 | Skin in the game + historial |

```
Quality Factor = (ER × 0.4) + (SR × 0.3) + (MW × 0.2) + (MQ × 0.1)

Example:
- Earnings Reliability: OE = $500M, Reported NI = $450M → Ratio 1.11 → Score 1.1
- Shenanigans Risk: Score 2/14 → Low risk → Score 1.15
- Moat Width: Wide moat → Score 1.2
- Management: Strong skin in game → Score 1.15

Quality Factor = (1.1 × 0.4) + (1.15 × 0.3) + (1.2 × 0.2) + (1.15 × 0.1)
             = 0.44 + 0.345 + 0.24 + 0.115
             = 1.14 (14% premium deserved)

If Peer Median P/E = 20x
Adjusted P/E for this company = 20 × 1.14 = 22.8x
```

---

## Paso 5.4: Rango de valoración implícito

### Desde los comparables (múltiplo × utilidades)

| Método | Múltiplo usado | Base de utilidades | Valor implícito |
|--------|-------------|---------------|--------------|
| P/E (reportado) | P/E mediano × Calidad | UN reportada | $X |
| P/OE | P/E mediano × Calidad | Owner Earnings | $Y |
| EV/EBITDA | EV/EBITDA mediano × Calidad | EBITDA | $Z (menos deuda neta) |

### Triangulación con el DCF

| Método | Valor implícito | Ponderación | Valor ponderado |
|--------|-------------|--------|---------------|
| DCF (caso base) | $X | 50% | $X × 0.5 |
| Comparables P/OE | $Y | 30% | $Y × 0.3 |
| Comparables EV/EBITDA | $Z | 20% | $Z × 0.2 |
| **Valor intrínseco combinado** | | **100%** | **$W** |

Las ponderaciones deben favorecer:
- El DCF cuando los OE son estables y predecibles
- Los comparables cuando el grupo de pares es acotado y representativo
- El EV/EBITDA cuando las estructuras de capital varían mucho

---

## Paso 5.5: Posicionamiento relativo

### ¿Dónde se ubica nuestra empresa?

| Métrica | Pct. 25 | Mediana | Pct. 75 | Nuestra empresa | Posición |
|--------|----------|--------|----------|-------------|----------|
| Crecimiento de ingresos | X% | X% | X% | X% | Sobre/Bajo la mediana |
| Margen de OE | X% | X% | X% | X% | Sobre/Bajo la mediana |
| ROIC | X% | X% | X% | X% | Sobre/Bajo la mediana |
| Deuda/EBITDA | Xx | Xx | Xx | Xx | Sobre/Bajo la mediana |
| P/E | Xx | Xx | Xx | Xx | Prima/Descuento |

### Narrativa
"La empresa X cotiza con [prima/descuento] frente a sus pares en base P/E, lo cual está [justificado/injustificado] porque [el margen de OE está sobre/bajo la mediana, el foso competitivo es más amplio/más estrecho, el crecimiento es más rápido/más lento]."

---

## Formato de salida

```markdown
## Comparables Analysis - {COMPANY}

### Peer Group
| Company | Ticker | Rationale for Inclusion |
|---------|--------|----------------------|
| {Peer 1} | {TICK} | {Why comparable} |

### Operating Metrics Comparison
[Table with all peers + statistics]

### Valuation Multiples
[Table with all peers + statistics]

### Quality-Adjusted Valuation
| Method | Raw Multiple | Quality Factor | Adjusted Multiple | Implied Value |
|--------|-------------|---------------|------------------|--------------|
| P/OE | {X}x | {X} | {X}x | ${X} |
| EV/EBITDA | {X}x | {X} | {X}x | ${X} |

### Relative Positioning
- Operating metrics: {above/at/below} median
- Valuation: {premium/at/discount} to peers
- Justified? {Yes/No} because {reason}

### Blended Valuation
- DCF Value: ${X} (50% weight)
- Comps Value: ${X} (50% weight)
- **Blended Intrinsic Value: ${X}**
```
