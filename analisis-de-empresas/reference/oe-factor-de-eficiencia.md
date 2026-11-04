# Owner Earnings - Factor de Eficiencia Tecnologica (PASO 5.5)

> **Parent Skill**: [SKILL.md](../SKILL.md)

---

**Concepto**: Algunas empresas estan en transicion de modelo de negocio o tecnologia que les permite operar con MENOS activos por unidad de output. En estos casos, el Suelo de Inflacion debe ajustarse por un Factor de Eficiencia.

> Este paso es OPCIONAL y solo aplica cuando hay evidencia clara de transicion tecnologica o cambio de modelo de negocio.

## Cuando Aplicar el Factor de Eficiencia

| Situacion | Aplica? | Ejemplo |
|-----------|---------|---------|
| Migracion a tecnologia mas eficiente | SI | Telco pasando de 3G/4G a 5G |
| Modelo asset-light con terceros | SI | Uso de infraestructura de partners (ej: Starlink) |
| Abandono de tecnologia legacy | SI | Cierre de red 2G/3G |
| Digitalizacion de canales | SI | Ventas online vs retail fisico |
| Consolidacion de infraestructura | SI | Data centers virtualizados |
| Empresa tradicional sin cambios | NO | Retail tradicional, manufactura clasica |
| Declive sin plan de eficiencia | NO | Industria en declive sin renovacion |

## Como Calcular el Factor de Eficiencia

```python
# Identificar componentes de eficiencia del MD&A o informes
# Cada componente tiene un descuento estimado sobre el Suelo

componentes_eficiencia = {
    'migracion_5g_fibra': 0.10,      # 5G requiere ~30% menos CAPEX/GB que 4G
    'abandono_legacy': 0.08,          # Red 2G/3G ya no requiere mantenimiento
    'asset_light': 0.07,              # Usa infraestructura de terceros
    'digitalizacion': 0.05,           # Menos inversion en retail fisico
    'consolidacion_infra': 0.05,      # Menos activos redundantes
}

# Factor de Eficiencia = 1 - suma de descuentos
factor_eficiencia = 1 - sum(componentes_eficiencia.values())
# Ejemplo: 1 - 0.35 = 0.65

# Suelo Ajustado por Eficiencia
suelo_ajustado = suelo_inflacion * factor_eficiencia
```

## Reglas de Aplicacion

1. **Conservadurismo**: El factor maximo razonable es 0.50 (50% de reduccion).
   Descuentos mayores requieren evidencia extraordinaria.

2. **Evidencia Requerida**: Para cada componente, debe haber mencion explicita en:
   - MD&A / Analisis Razonado
   - Notas sobre estrategia de CAPEX
   - Comunicados de prensa sobre eficiencias

3. **Validacion por Resultados**: Si el servicio se deteriora (clientes cayendo,
   satisfaccion bajando), el factor de eficiencia debe reducirse o eliminarse.

4. **Punto de Equilibrio**: Calcular siempre el factor minimo necesario para OE = 0.
   Si el factor requerido es > 50%, probablemente hay sub-inversion real.

## Tabla de Referencia: Descuentos por Industria

| Industria | Transicion Tipica | Descuento Maximo |
|-----------|-------------------|------------------|
| Telecomunicaciones | 4G→5G, cobre→fibra | 35-45% |
| Banca | Sucursales→digital | 30-40% |
| Retail | Tiendas→e-commerce | 25-35% |
| Media | Impreso→digital | 40-50% |
| Energia | Fosil→renovable | 20-30% |
| Manufactura | Manual→automatizada | 15-25% |

## Ejemplo Real: ENTEL 2025 (Telco en Transicion 5G)

```
EVIDENCIA DE EFICIENCIAS (del Analisis Razonado):
1. "5G desplegado en todas las regiones" → 5G mas eficiente que 4G
2. "Menores inversiones en redes 2G y 3G" → Abandono de legacy
3. "Direct to Cell con Starlink" → Asset-light para nuevas coberturas
4. "30% ventas en canales digitales" → Menos retail fisico
5. "Fibra Hogar +14%" → Fibra mas eficiente que inalambrico

CALCULO FACTOR DE EFICIENCIA:
+----------------------------------+------------+
| Componente                       | Descuento  |
+----------------------------------+------------+
| Migracion 5G/Fibra               |    10%     |
| Abandono 2G/3G                   |     8%     |
| Asset-light (Starlink, Wi-Net)   |     7%     |
| Digitalizacion canales           |     5%     |
| Consolidacion fibra vs wireless  |     5%     |
+----------------------------------+------------+
| TOTAL DESCUENTO                  |    35%     |
| FACTOR EFICIENCIA                |    0.65    |
+----------------------------------+------------+

VALIDACION POR RESULTADOS:
- Ookla: #1 en velocidad Chile ✓ (servicio no deteriorado)
- Satisfaccion: #1 Procalidad ✓ (calidad mantenida)
- Clientes Chile: -4% ✗ (cierta erosion)
- Prepago: -32% ✗ (segmento abandonado)

AJUSTE POR VALIDACION:
Los resultados mixtos sugieren usar factor conservador.
Factor Final Recomendado: 0.65 (35% eficiencia)

SUELO AJUSTADO:
Suelo Original (con volumen):     M$ 968,293
Factor Eficiencia:                × 0.65
Suelo Ajustado:                   M$ 629,390

OWNER EARNINGS CORREGIDOS:
Net Income Ajustado:              M$   89,153
+ D&A + Deterioro:                M$  585,619
- CAPEX Mant. (Suelo Ajustado):   M$ (629,390)
───────────────────────────────────────────────
= OWNER EARNINGS:                 M$   45,382  ← POSITIVO

vs Sin ajuste:                    M$ (293,521) ← NEGATIVO

INTERPRETACION:
Con el Factor de Eficiencia de 35%, ENTEL pasa de destruir
valor a generar un OE marginal de 1.5%. La brecha de CAPEX
se reduce de 45% a 15%.
```

## Codigo Python

```python
def calcular_factor_eficiencia(evidencia_mda):
    """
    Calcula el Factor de Eficiencia basado en evidencia del MD&A.

    Args:
        evidencia_mda: dict con componentes identificados y sus descuentos
        Ejemplo: {'migracion_5g': 0.10, 'abandono_legacy': 0.08}

    Returns:
        float: Factor de eficiencia entre 0.50 y 1.00
    """
    descuento_total = sum(evidencia_mda.values())

    # Cap maximo de 50% de descuento
    descuento_total = min(descuento_total, 0.50)

    factor_eficiencia = 1 - descuento_total

    return factor_eficiencia


def ajustar_suelo_por_eficiencia(suelo_inflacion, factor_eficiencia,
                                  validacion_servicio=True):
    """
    Ajusta el Suelo de Inflacion por el Factor de Eficiencia.

    Args:
        suelo_inflacion: Suelo calculado en PASO 5
        factor_eficiencia: Factor de PASO 5.5 (entre 0.50 y 1.00)
        validacion_servicio: True si el servicio no se ha deteriorado

    Returns:
        float: Suelo ajustado por eficiencia
    """
    if not validacion_servicio:
        # Si el servicio se deteriora, aplicar solo 50% del descuento
        factor_ajustado = 1 - ((1 - factor_eficiencia) * 0.5)
    else:
        factor_ajustado = factor_eficiencia

    suelo_ajustado = suelo_inflacion * factor_ajustado

    return suelo_ajustado
```

## Cuando NO Aplicar el Factor de Eficiencia

| Situacion | Por Que No Aplica |
|-----------|-------------------|
| Clientes cayendo >10% anual | Eficiencia no compensa perdida de mercado |
| NPS/Satisfaccion cayendo | Servicio deteriorado = sub-inversion real |
| Competidores ganando share | Mercado castiga falta de inversion |
| Analistas/Rating alertan | Terceros ven problema que empresa niega |
| CAPEX/D&A < 0.70 por 3+ años | Sub-inversion estructural, no eficiencia |

## Matriz de Decision Final

```
                    ┌─────────────────────────────────┐
                    │   EVIDENCIA DE EFICIENCIAS?     │
                    └─────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
                   SI                            NO
                    │                             │
        ┌───────────┴───────────┐                 │
        ▼                       ▼                 ▼
   SERVICIO OK?           SERVICIO MAL?     SIN AJUSTE
        │                       │           (Factor=1.0)
        ▼                       ▼
   Factor 0.50-0.80       Factor 0.75-0.90
   (Aplicar completo)     (Aplicar parcial)
```
