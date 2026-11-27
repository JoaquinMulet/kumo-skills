# Plantillas de salida

Estructura exacta de los tres informes finales.

---

## Salida 1: Informe de la revisión forense

El cuerpo del informe es el anexo de 15 veredictos, con el formato exacto que da
`forense-procedimiento.md` y validado por `scripts/validar_forense.py`. Antes del anexo va este
resumen, y después la síntesis de `fase3-sintesis.md`.

```markdown
# Revisión forense. {EMPRESA}, {PERÍODO}

{Una frase con la conclusión, en palabras del negocio. Qué parte del resultado no se entiende o no
se repite, y qué estaría tapando.}

| Dato | Valor |
|---|---|
| Puntaje | {N} puntos, tramo «{Limpio, Dudas, Dudas importantes o Manipulación seria}» |
| Hallazgos | {N}, el mayor de veredicto {VEREDICTO} |
| Pruebas sin dato | {códigos, y qué falta} |
| Efecto en la tasa de descuento | {lo que diga la tabla del puntaje} |

| Cifra | Reportada | Ajustada | De qué pruebas sale |
|---|---|---|---|
| Utilidad neta | {X} | {Y} | {códigos} |
| Flujo operacional | {X} | {Y} | {códigos} |
| Patrimonio | {X} | {Y} | {códigos} |

Documentos revisados. {lista, con el período de cada uno}
```

---

## Salida 2: Informe de owner earnings

```markdown
# Owner Earnings Analysis - {COMPANY} {PERIOD}

## Executive Summary

```
+================================================================+
|                                                                |
|   OWNER EARNINGS: M$ {VALUE}                                   |
|   OE MARGIN: {X.X}%                                            |
|   OE PER SHARE: ${VALUE}                                       |
|                                                                |
|   Assessment: {CREATES VALUE | DESTROYS VALUE | MARGINAL}      |
|                                                                |
+================================================================+
```

### Key Metrics Comparison

| Metric | Reported | Owner Earnings Basis | Difference |
|--------|----------|---------------------|------------|
| Net Income | M${X} | M${Y} (Adjusted) | {-X%} |
| EPS | ${X} | ${Y} (OE/Share) | {-X%} |
| P/E | {X}x | {Y}x (P/OE) | |
| Earnings Yield | {X}% | {Y}% (OE Yield) | |

---

## 1. Calculation Waterfall

```
REPORTED NET INCOME:                    M$ {X}
                                        ─────────
ADJUSTMENTS FROM THE FORENSIC REVIEW (PASO 4):
- {Adjustment 1 description}:           M$ ({X})    <- {Reference}
- {Adjustment 2 description}:           M$ ({X})    <- {Reference}
                                        ─────────
= ADJUSTED NET INCOME:                  M$ {X}
                                        ─────────

NON-CASH ITEMS (ADD BACK):
+ Depreciation - PPE:                   M$ {X}      <- Note {X}
+ Depreciation - ROU Assets:            M$ {X}      <- Note {X}
+ Amortization - Intangibles:           M$ {X}      <- Note {X}
+ Impairment Charges:                   M$ {X}      <- Note {X}
+ {Other non-cash items}:               M$ {X}      <- {Source}
                                        ─────────
Subtotal Non-Cash:                      M$ {X}
                                        ─────────

MAINTENANCE CAPEX (SUBTRACT):
- Maintenance CAPEX:                    M$ ({X})    <- See Section 2
                                        ═════════
= OWNER EARNINGS:                       M$ {X}
                                        ═════════

OE Margin = {OE} / {Revenue} = {X.X}%
OE per Share = {OE} / {Shares} = ${X.XX}
```

---

## 2. Maintenance CAPEX Calculation

### Step 1: Asset Age

| Component | Value | Source |
|-----------|-------|--------|
| Accumulated Depreciation | M$ {X} | Note {X}, Page {Y} |
| Annual Depreciation | M$ {X} | Note {X}, Page {Y} |
| **Asset Age** | **{X.X} years** | Calculated |

```
Asset Age = {Accum Depr} / {Annual Depr} = {X.X} years
```

### Step 2: Geographic Inflation Weighting

| Geography | Revenue | Weight | Local Inflation | Weighted |
|-----------|---------|--------|-----------------|----------|
| {Country 1} | M${X} | {X}% | {X.X}% | {X.XX}% |
| {Country 2} | M${X} | {X}% | {X.X}% | {X.XX}% |
| {Country 3} | M${X} | {X}% | {X.X}% | {X.XX}% |
| **Total** | M${X} | 100% | | **{X.XX}%** |

Source: Segment Note {X}; Inflation data from {sources}

### Step 3: Inflation Factor

```
Inflation Factor = (1 + {blended inflation})^{asset age}
                 = (1 + {X.XXX})^{X.X}
                 = {X.XX}
```

**Interpretation**: Replacing assets today costs {X}% more than historical book value.

### Step 4: Inflation Floor (Base)

```
Floor Base = D&A Total × Inflation Factor
           = M$ {D&A} × {factor}
           = M$ {FLOOR_BASE}
```

### Step 5: Volume Adjustment (if applicable)

| Volume Metric | Current | Peak | Utilization |
|---------------|---------|------|-------------|
| {Subscribers/Units/etc.} | {X} | {X} | {X.X}% |

```
Adjusted Floor = Floor Base × Utilization Ratio
               = M$ {FLOOR_BASE} × {X.X}%
               = M$ {ADJUSTED_FLOOR}
```

{If volume is growing, skip this step and use Floor Base}

### Step 6: Alpha Method Comparison

```
Alpha = Gross PPE / Revenue = M${X} / M${Y} = {X.XX}

Volume Growth: {X}% (from MD&A KPIs)
Price Growth: {X}% (from MD&A)
Real Volume Growth: {Volume - Price}% = {X}%
```

{If real volume growth <= 0}:
```
Alpha Method Result: ALL CAPEX = Maintenance = M$ {CAPEX}
Reason: Volume declining, no growth CAPEX justified
```

{If real volume growth > 0}:
```
Growth CAPEX = Alpha × ΔVolume Revenue = {X.XX} × M${Y} = M$ {Z}
Maintenance CAPEX (Alpha) = Total CAPEX - Growth CAPEX = M$ {W}
```

### Step 7: MAX Rule Application

```
┌──────────────────────────────────────────────────────────────┐
│  MAINTENANCE CAPEX = MAX(Alpha Method, Inflation Floor)      │
│                                                              │
│  Alpha Method Result:    M$ {X}                              │
│  Inflation Floor:        M$ {Y}                              │
│                                                              │
│  RESULT: M$ {MAX}  <- {Which method won}                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Investment Gap Analysis

| Metric | Value | Assessment |
|--------|-------|------------|
| Actual CAPEX | M$ {X} | What company spent |
| Required (Floor) | M$ {Y} | What's needed to maintain |
| **Gap** | **M$ ({Z})** | **{X}% underinvestment** |
| CAPEX / D&A Ratio | {X.XX}x | {Assessment} |
| CAPEX / Floor Ratio | {X.XX}x | {Assessment} |

### Investment Gap Interpretation

{Analysis of whether underinvestment is:}
- Strategic harvest mode (intentional)
- Financial constraint (forced)
- Temporary optimization
- Chronic erosion

{Include evidence for your conclusion}

---

## 4. Scenario Analysis

| Scenario | Maintenance CAPEX | Owner Earnings | OE Margin | Assessment |
|----------|-------------------|----------------|-----------|------------|
| Pessimistic | M$ {X} | M$ {Y} | {Z}% | {Description} |
| **Base** | **M$ {X}** | **M$ {Y}** | **{Z}%** | **{Description}** |
| Optimistic | M$ {X} | M$ {Y} | {Z}% | {Description} |

### Scenario Definitions

- **Pessimistic**: Full inflation floor without volume adjustment
- **Base**: Inflation floor with volume adjustment (recommended)
- **Optimistic**: Actual CAPEX as maintenance (assumes efficiency)

---

## 5. Valuation Implications

### Using Owner Earnings

| Metric | Reported Basis | OE Basis | Note |
|--------|---------------|----------|------|
| EPS | ${X} | ${Y} | OE per share |
| P/E | {X}x | {Y}x | P/OE ratio |
| Earnings Yield | {X}% | {Y}% | OE Yield |

### Adjusted Equity

| Component | Value |
|-----------|-------|
| Reported Equity | M$ {X} |
| - Irrecoverable DTA | M$ ({Y}) |
| - Other Adjustments | M$ ({Z}) |
| **Adjusted Equity** | **M$ {W}** |

### Valuation Summary

{If OE positive}:
```
At current price of ${X}, the stock trades at:
- P/OE: {Y}x
- OE Yield: {Z}%

This {compares favorably/unfavorably} to {benchmark/hurdle rate}.
```

{If OE negative}:
```
Owner Earnings are NEGATIVE, indicating the company destroys value.
No meaningful P/OE ratio can be calculated.
Valuation should focus on:
- Liquidation value
- Turnaround potential
- Strategic acquisition value
```

---

## 6. Data Sources

| Data Point | Value | Document | Location |
|------------|-------|----------|----------|
| Gross PPE | M$ {X} | Note {Y} | Page {Z} |
| Accumulated Depreciation | M$ {X} | Note {Y} | Page {Z} |
| Total D&A | M$ {X} | Income Statement | Line {Z} |
| Total CAPEX | M$ {X} | Cash Flow | Line {Z} |
| Revenue | M$ {X} | Income Statement | Line {Z} |
| Net Income | M$ {X} | Income Statement | Line {Z} |
| Shares Outstanding | {X} | Note {Y} | Page {Z} |
| Share Price | ${X} | Market Data | As of {Date} |

---

**Analysis Date**: {Date}
**Framework**: Owner Earnings (Buffett) + Inflation Adjustment (Greenwald)
**Skills Used**: analisis-de-empresas
```

---

## Salida 3: Documento de preguntas al CFO

```markdown
# Questions for Management - {COMPANY} {PERIOD}

## Priority Matrix

| Priority | # | Topic | Severity | Materiality | Category |
|----------|---|-------|----------|-------------|----------|
| 1 | Q1 | {Topic} | {SEVERITY} | {X}% of {Metric} | {EM/CF/KM/AA/OE} |
| 2 | Q2 | {Topic} | {SEVERITY} | {X}% of {Metric} | {Category} |
| 3 | Q3 | {Topic} | {SEVERITY} | {X}% of {Metric} | {Category} |
| 4 | Q4 | {Topic} | {SEVERITY} | {X}% of {Metric} | {Category} |

---

## Question 1: {Topic}

### Classification
| Field | Value |
|-------|-------|
| Priority | 1 |
| Severity | {CRITICAL / HIGH / MEDIUM} |
| Category | {EM / CF / KM / AA / OE} |
| Related Finding | {Technique ID} |
| Materiality | {X}% of {Net Income / Equity / CFFO} |

### Context (Objective Data from Filings)

| Metric | Value | Source | Calculation |
|--------|-------|--------|-------------|
| {Metric 1} | {Value} | Note {X}, Page {Y} | Direct |
| {Metric 2} | {Value} | Note {X}, Page {Y} | Direct |
| {Derived Metric} | {Value} | Calculated | {Formula} |

### The Question

> "{Full question text. Requirements:
> - Uses specific numbers from their filings
> - References exact notes or pages
> - Cannot be dismissed as factually incorrect
> - Requires substantive explanation, not deflection
> - Is professionally worded but pointed}"

### Why This Question Must Be Answered

1. **Data Source**: All figures from Note {X} and {Y} - their own disclosures
2. **Materiality**: Represents {X}% of {metric}, exceeding 5% threshold
3. **Disclosure Gap**: Not explained in MD&A section {X}
4. **Valuation Impact**: Affects {P/E, P/B, DCF, etc.} by approximately {X}%
5. **Audit Focus**: {If applicable: Auditor flagged as Key Audit Matter}

### Anticipated Responses & Counter-Arguments

| If management says... | Counter with... |
|----------------------|-----------------|
| "This is standard accounting treatment under {GAAP/IFRS}" | "Standard treatment doesn't address the economic substance. Specifically, {data point} suggests {issue}. How do you reconcile this?" |
| "We expect improvement in future periods" | "Based on what specific projections? Current trajectory of {metric} suggests {X} years to achieve that. Can you share the documented assumptions?" |
| "This is a one-time/non-recurring item" | "Similar items appeared in {FY20XX, FY20XX}. At what point do recurring 'non-recurring' items become part of normalized results?" |
| "Our auditors reviewed and approved this" | "Auditor approval confirms GAAP compliance, not commercial reasonableness. The auditor's Key Audit Matter on this topic notes {specific concern}. How does management address that concern?" |
| "We can discuss offline" | "Given the materiality ({X}% of {metric}), public shareholders deserve a public answer. Can you provide at least a high-level response now?" |

### Follow-up Questions

1. "{Drill deeper into same issue}"
2. "{Request specific documentation}"
3. "{Connect to related finding}"

---

## Question 2: {Topic}

{Same structure as Question 1}

---

## Question 3: {Topic}

{Same structure}

---

## Question 4: {Topic}

{Same structure}

---

## Questions by Category

### Earnings Quality
- Q{N}: {Brief description}
- Q{N}: {Brief description}

### Cash Flow Authenticity
- Q{N}: {Brief description}

### Capital Allocation
- Q{N}: {Brief description}

### Asset Quality
- Q{N}: {Brief description}

### Forward Guidance
- Q{N}: {Brief description}

---

## Appendix: Source Document Cross-Reference

| Question | Primary Sources | Specific References |
|----------|----------------|---------------------|
| Q1 | {Document} | Note {X}, p.{Y}; Note {Z}, p.{W} |
| Q2 | {Document} | {References} |
| Q3 | {Document} | {References} |
| Q4 | {Document} | {References} |

---

## Preparation Notes

### Before the Call
- [ ] Verify all data points are current
- [ ] Prepare printed copies of referenced notes
- [ ] Have follow-up questions ready
- [ ] Note time constraints (prioritize Q1-Q2)

### During the Call
- [ ] State data source before asking question
- [ ] Note exact response for follow-up
- [ ] If deflected, use counter-argument
- [ ] Request documentation for vague answers

### After the Call
- [ ] Document all responses
- [ ] Compare to prior guidance
- [ ] Update analysis if new information provided
- [ ] Flag any inconsistencies for further research

---

**Prepared**: {Date}
**For Use In**: {Earnings Call / Investor Meeting / Written Inquiry}
**Based On**: {COMPANY} {PERIOD} Financial Statements and MD&A
```

---

## Convención de nombres de archivo

```
{COMPANY}_{TYPE}_{PERIOD}.md

Examples:
- ACME_Revision_Forense_Q4_2025.md
- ACME_Owner_Earnings_Q4_2025.md
- ACME_CFO_Questions_Q4_2025.md
```

Todos los archivos van en el subdirectorio `output/` de la carpeta de trabajo.
