# Owner Earnings - Template de Codigo Python

> **Parent Skill**: [SKILL.md](../SKILL.md)

---

```python
import pandas as pd
import numpy as np

def calcular_factor_eficiencia(evidencia_mda, validacion_servicio=True):
    """
    PASO 5.5: Calcula el Factor de Eficiencia basado en evidencia del MD&A.

    Args:
        evidencia_mda: dict con componentes identificados y sus descuentos
        Ejemplo: {'migracion_5g': 0.10, 'abandono_legacy': 0.08}
        validacion_servicio: True si metricas de servicio no se deterioran

    Returns:
        float: Factor de eficiencia entre 0.50 y 1.00
    """
    if not evidencia_mda:
        return 1.0  # Sin ajuste

    descuento_total = sum(evidencia_mda.values())

    # Cap maximo de 50% de descuento
    descuento_total = min(descuento_total, 0.50)

    # Si servicio se deteriora, aplicar solo 50% del descuento
    if not validacion_servicio:
        descuento_total = descuento_total * 0.5

    factor_eficiencia = 1 - descuento_total

    return factor_eficiencia


def calcular_owner_earnings(df, inflacion_promedio=0.029, incluir_sbc=True,
                           factor_eficiencia=1.0):
    """
    Calcula Owner Earnings usando framework Greenwald-Buffett.

    Args:
        df: DataFrame con columnas requeridas (ver PASO 1)
        inflacion_promedio: Inflacion historica promedio (default 2.9% USA)
        incluir_sbc: Si True, suma SBC como no-cash (clasico).
                     Si False, lo deja como gasto (conservador para tech)
        factor_eficiencia: Factor de PASO 5.5 (default 1.0 = sin ajuste).
                          Valores tipicos: 0.65-0.85 para empresas en transicion.

    Returns:
        DataFrame con Owner Earnings y metricas calculadas
    """

    # PASO 2: Alpha
    df['alpha'] = df['ppe_bruto'] / df['ventas']
    df['alpha_5y'] = df['alpha'].rolling(window=5, min_periods=3).mean()

    # PASO 3: Delta ventas por volumen
    df['delta_ventas_volumen'] = np.where(
        df['crec_volumen_pct'] > 0,
        df['ventas'].shift(1) * (df['crec_volumen_pct'] / 100),
        0
    )

    # PASO 4: Edad de activos
    df['edad_activos'] = df['depreciacion_acumulada'] / df['depreciacion']

    # PASO 5: Suelo de inflacion
    df['factor_inflacion'] = (1 + inflacion_promedio) ** df['edad_activos']
    df['mc_floor_base'] = df['depreciacion'] * df['factor_inflacion']

    # PASO 5.5: Aplicar Factor de Eficiencia (si aplica)
    df['factor_eficiencia'] = factor_eficiencia
    df['mc_floor'] = df['mc_floor_base'] * factor_eficiencia

    # PASO 6: CAPEX crecimiento organico
    df['capex_crecimiento_organico'] = df['alpha_5y'] * df['delta_ventas_volumen']
    df['capex_crecimiento_organico'] = df['capex_crecimiento_organico'].fillna(0)

    # PASO 7: Separacion final
    df['sub_inversion'] = df['mc_floor'] > df['capex_ppe']

    df['capex_disponible_crecimiento'] = np.where(
        df['sub_inversion'], 0,
        df['capex_ppe'] - df['mc_floor']
    )

    df['capex_crecimiento_organico_efectivo'] = np.minimum(
        df['capex_crecimiento_organico'],
        df['capex_disponible_crecimiento']
    )

    df['capex_mantenimiento'] = np.where(
        df['sub_inversion'],
        df['mc_floor'],
        df['capex_ppe'] - df['capex_crecimiento_organico_efectivo']
    )

    # REGLA DEL MAXIMO: Siempre usar el mayor entre calculo Alpha y Piso
    df['capex_mantenimiento'] = np.maximum(
        df['capex_mantenimiento'],
        df['mc_floor']
    )

    df['capex_crecimiento_total'] = (
        df['capex_crecimiento_organico_efectivo'] + df['adquisiciones']
    )

    # PASO 8: Ajustes de partidas no monetarias
    # Rellenar columnas opcionales con 0 si no existen
    columnas_opcionales = [
        'sbc', 'amort_intangibles_ma', 'impuestos_diferidos_cambio',
        'impairments', 'cargos_reestructuracion',
        'perdidas_no_realizadas', 'ganancias_no_realizadas'
    ]
    for col in columnas_opcionales:
        if col not in df.columns:
            df[col] = 0

    # Ajustes a SUMAR (no salieron en efectivo)
    df['ajustes_sumar'] = (
        df['depreciacion'] +
        df['amortizacion'] +
        (df['sbc'] if incluir_sbc else 0) +
        df['amort_intangibles_ma'] +
        df['impuestos_diferidos_cambio'].clip(lower=0) +  # Solo incrementos
        df['impairments'] +
        df['cargos_reestructuracion'] +
        df['perdidas_no_realizadas']
    )

    # Ajustes a RESTAR
    df['ajustes_restar'] = (
        df['ganancias_no_realizadas'] +
        (-df['impuestos_diferidos_cambio']).clip(lower=0) +  # Solo decrementos
        df['capex_mantenimiento']
    )

    # PASO 9: Owner Earnings Finales
    df['owner_earnings'] = (
        df['utilidad_neta'] +
        df['ajustes_sumar'] -
        df['ajustes_restar']
    )
    df['owner_earnings_margin'] = df['owner_earnings'] / df['ventas'] * 100

    # Metricas de calidad
    df['sbc_pct_utilidad'] = df['sbc'] / df['utilidad_neta'] * 100
    df['calidad_alta'] = (
        (df['sbc_pct_utilidad'] < 10) &
        (df['impairments'] < df['utilidad_neta'] * 0.05) &
        (~df['sub_inversion'])
    )

    return df


def calcular_roiic(df):
    """
    Calcula ROIIC (Return on Incremental Invested Capital).
    Requiere columnas: utilidad_operativa, tasa_impositiva, capex_crecimiento_total
    """
    # NOPAT
    df['nopat'] = df['utilidad_operativa'] * (1 - df['tasa_impositiva'])

    # Ventana de 3 anos
    df['nopat_3y_sum'] = df['nopat'].rolling(window=3, min_periods=3).sum()
    df['nopat_incremental'] = df['nopat_3y_sum'] - df['nopat_3y_sum'].shift(3)

    df['capex_crec_3y'] = df['capex_crecimiento_total'].rolling(window=3).sum()
    df['capex_crec_3y_lag'] = df['capex_crec_3y'].shift(1)

    df['roiic'] = np.where(
        df['capex_crec_3y_lag'] > 0,
        df['nopat_incremental'] / df['capex_crec_3y_lag'] * 100,
        np.nan
    )

    return df
```

## Uso para Valoracion DCF

```python
# Proyeccion simplificada
ventas_proyectadas = ventas_actual * (1 + growth_rate) ** anos

# Owner Earnings proyectados (usando margen historico)
oe_margin_promedio = df['owner_earnings_margin'].mean() / 100
oe_proyectados = ventas_proyectadas * oe_margin_promedio

# Valor presente
discount_rate = wacc - growth_perpetuo
valor_presente = oe_proyectados / ((1 + discount_rate) ** anos)

# Precio por accion
precio_intrinseco = sum(valor_presente) / acciones_outstanding
```
