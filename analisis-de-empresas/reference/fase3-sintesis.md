# Fase 3: Síntesis

Cómo consolidar los hallazgos de los 4 agentes y generar las preguntas para el CFO.

---

## Paso 3.1: Reunir los resultados de los agentes

Cuando la Fase 2 termine, debes tener:

```
analysis/
+-- agent1_em_findings.md   # 7 techniques
+-- agent2_cf_findings.md   # 3 techniques
+-- agent3_km_findings.md   # 2 techniques
+-- agent4_aa_findings.md   # 2 techniques
```

---

## Paso 3.2: Crear la tabla resumen

Consolida todos los hallazgos en una sola tabla:

```markdown
## Findings Summary

| # | Category | Technique | Status | Severity | Impact | NI Effect | CF Effect | Equity Effect |
|---|----------|-----------|--------|----------|--------|-----------|-----------|---------------|
| 1 | EM | EM-1: Revenue Too Soon | NOT DETECTED | - | - | - | - | - |
| 2 | EM | EM-2: Bogus Revenue | NOT DETECTED | - | - | - | - | - |
| 3 | EM | EM-3: One-Time Gains | DETECTED | HIGH | M$102,243 | -53% | 0 | 0 |
| 4 | EM | EM-4: Shift Expenses Later | NOT DETECTED | - | - | - | - | - |
| 5 | EM | EM-5: Reduce Liabilities | NOT DETECTED | - | - | - | - | - |
| 6 | EM | EM-6: Shift Income Later | NOT DETECTED | - | - | - | - | - |
| 7 | EM | EM-7: Big Bath | NOT DETECTED | - | - | - | - | - |
| 8 | CF | CF-1: Financing to Operating | NOT DETECTED | - | - | - | - | - |
| 9 | CF | CF-2: Operating to Other | NOT DETECTED | - | - | - | - | - |
| 10 | CF | CF-3: Unsustainable Boost | DETECTED | LOW | M$77,910 | 0 | -9% | 0 |
| 11 | KM | KM-1: Misleading Metrics | DETECTED | HIGH | Qualitative | N/A | N/A | N/A |
| 12 | KM | KM-2: Balance Sheet Distortion | NOT DETECTED | - | - | - | - | - |
| 13 | AA | AA-1: Boost Acquired Earnings | NOT DETECTED | - | - | - | - | - |
| 14 | AA | AA-2: Inflate Cash Flow | DETECTED | CRITICAL | M$562,300 | 0 | 0 | -29% |
```

---

## Paso 3.3: Crear la matriz de referencias cruzadas

Vincula los hallazgos relacionados para mostrar cómo se acumulan:

```markdown
## Cross-Reference Matrix

| Finding | Primary Impact | Secondary Effects | Related Findings | OE Adjustment Needed |
|---------|---------------|-------------------|------------------|---------------------|
| EM-3: Tax Benefit M$102K | Inflates NI by 53% | Misleads ROE, EPS | KM-1 (metrics) | Subtract from NI |
| CF-3: Payables Stretch | Boosts CFFO 9% | May reverse next period | None | Monitor only |
| KM-1: EBITDA Focus | Hides capex reality | Misleads valuation | AA-2 (DTA) | Use OE not EBITDA |
| AA-2: DTA Peru M$562K | Inflates equity 29% | Hides operating loss | EM-3 (related) | Write off in OE |

## Compound Effect Analysis

The findings interact as follows:

1. **Reported Net Income**: M$191,396
   - Less: Non-recurring tax benefit (EM-3): -M$102,243
   - **Adjusted Net Income**: M$89,153 (-53% lower)

2. **Reported Equity**: M$1,943,297
   - Less: Irrecoverable DTA (AA-2): -M$562,300
   - **Adjusted Equity**: M$1,380,997 (-29% lower)

3. **Derived Metrics**:
   - Reported ROE: 9.8%
   - Adjusted ROE: 6.5%
```

---

## Paso 3.4: Calcular la evaluación global

### Puntaje de severidad

| Severidad | Puntos |
|-----------|--------|
| LOW | 1 |
| MEDIUM | 2 |
| HIGH | 3 |
| CRITICAL | 4 |

### Calcular el puntaje total

```
Total Score = Sum of (Severity Points for each DETECTED finding)

Example:
- EM-3 (HIGH): 3 points
- CF-3 (LOW): 1 point
- KM-1 (HIGH): 3 points
- AA-2 (CRITICAL): 4 points
-----------------------
Total: 11 points

Interpretation:
- 0-3 points: LOW overall risk
- 4-7 points: MEDIUM overall risk
- 8-12 points: HIGH overall risk
- 13+ points: CRITICAL overall risk
```

---

## Paso 3.5: Generar las preguntas para el CFO

Para cada hallazgo con severidad >= MEDIUM, crea una pregunta con esta plantilla:

### Plantilla de pregunta

```markdown
## Question {N}: {Topic}

### Severity: {MEDIUM | HIGH | CRITICAL}
### Related Finding: {EM-X, CF-X, KM-X, or AA-X}

---

### Context (Objective Data from Filings)

| Metric | Value | Source |
|--------|-------|--------|
| {Metric 1} | {Value} | Note {X}, Page {Y} |
| {Metric 2} | {Value} | {Document}, {Location} |
| {Derived Metric} | {Value} | Calculated: {Formula} |

---

### The Question

> "{Write the exact question here. It should:
> - Use specific numbers from their own filings
> - Reference the exact note or page
> - Be impossible to dismiss as 'incorrect data'
> - Require a substantive answer, not a deflection}"

---

### Why This Question Must Be Answered

1. **Uses their own data**: All figures come from Note {X} and {Y}
2. **Material impact**: Represents {X}% of {Net Income / Equity / CFFO}
3. **Not addressed in MD&A**: Management did not explain this discrepancy
4. **Affects valuation**: Impacts {P/E, P/B, DCF} by {X}%

---

### Anticipated Responses & Counter-Arguments

| If management says... | Respond with... |
|----------------------|-----------------|
| "This is standard accounting treatment" | "Standard treatment doesn't explain why the economic substance differs from the accounting. Specifically, {counter-point}..." |
| "We expect to recover this in the future" | "What are the specific, documented projections? Current run-rate suggests {X} years to recover." |
| "This is a one-time item" | "Similar 'one-time' items appeared in {prior years}. When should we expect normalized results?" |
| "Our auditors approved this" | "Auditor approval doesn't mean it's the right estimate. The auditor flagged this as a Key Audit Matter because {reason}." |

---

### Follow-up Questions (if initial response is evasive)

1. "{Follow-up that drills deeper}"
2. "{Alternative angle on same issue}"
3. "{Request for specific documentation}"
```

---

## Paso 3.6: Priorizar las preguntas

Ordena las preguntas por:

1. **Materialidad** (% de la utilidad neta, el patrimonio o el CFFO)
2. **Severidad** (CRITICAL > HIGH > MEDIUM)
3. **Recuperabilidad** (¿el problema se puede corregir o es permanente?)

### Matriz de prioridades

```markdown
## CFO Questions - Priority Matrix

| Priority | Question # | Topic | Severity | Materiality | Category |
|----------|-----------|-------|----------|-------------|----------|
| 1 | Q1 | DTA Recoverability | CRITICAL | 29% Equity | AA |
| 2 | Q2 | Tax Benefit Sustainability | HIGH | 53% of NI | EM |
| 3 | Q3 | CAPEX vs Depreciation Gap | HIGH | Qualitative | KM |
| 4 | Q4 | Payables Extension | LOW | 9% CFFO | CF |
```

---

## Paso 3.7: Vincular con los Owner Earnings

Asegúrate de que los hallazgos de manipulaciones contables pasen al cálculo de Owner Earnings:

```markdown
## Adjustments for Owner Earnings Calculation

Based on Shenanigans Analysis:

| Finding | OE Adjustment | Amount | Rationale |
|---------|---------------|--------|-----------|
| EM-3: Tax Benefit | Subtract from NI | -M$102,243 | Non-recurring, no cash |
| AA-2: DTA Peru | Note for equity adj | N/A | Affects book value, not OE |
| KM-1: EBITDA Focus | Use OE instead | N/A | Methodology, not adjustment |

### Adjusted Starting Point for Owner Earnings

Reported Net Income:          M$ 191,396
- Non-recurring tax benefit:  M$(102,243)  ← From EM-3
---------------------------------
Adjusted Net Income:          M$  89,153   ← Use this for OE
```

---

## Ejemplo: salida completa de la síntesis

```markdown
# Synthesis Report - ACME Corp Q4 2025

## Executive Summary

| Metric | Value |
|--------|-------|
| Techniques Applied | 14 |
| Issues Detected | 4 |
| Overall Severity | HIGH (11 points) |
| Material Findings | 3 |
| CFO Questions Generated | 4 |

## Key Findings

1. **53% of Net Income is Non-Recurring** (EM-3, HIGH)
   - Tax benefit from intragroup transaction lacks economic substance

2. **29% of Equity at Risk** (AA-2, CRITICAL)
   - DTA in Peru would take 99,000+ years to recover

3. **EBITDA Misleads Investors** (KM-1, HIGH)
   - Owner Earnings actually negative after proper capex treatment

4. **Payables Being Stretched** (CF-3, LOW)
   - Minor boost to CFFO, may reverse

## Adjusted Metrics

| Metric | Reported | Adjusted | Change |
|--------|----------|----------|--------|
| Net Income | M$191,396 | M$89,153 | -53% |
| Equity | M$1,943,297 | M$1,380,997 | -29% |
| ROE | 9.8% | 6.5% | -34% |

## CFO Questions (Priority Order)

1. DTA Recoverability in Peru
2. Tax Benefit Economic Substance
3. CAPEX Sustainability
4. Working Capital Strategy

See full question details in CFO Questions document.
```
