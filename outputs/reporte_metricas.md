# Reporte Estadístico de Métricas AP1 vs AP2

Generado: 2025-12-07 18:20

Fuente CSV: `data/Estudiantes_2023-2024_con_metricas_sonarcloud.csv`

## Resumen Global

Se analizaron 10 métricas. 6 resultaron significativas tras corrección FDR (α=0.05).

- Mejoras significativas: 4 -> security_rating, vulnerabilities, bugs, reliability_rating
- Deterioros significativos: 1 -> cognitive_complexity
- Cambios significativos pero neutros (contexto): 1 -> ncloc

## Principales Cambios (Top |d|)

- security_rating: d=-0.751 (mediano), p_FDR=1.58e-05, ↓ cambio relativo NA (AP1=2.93, AP2=1.23) -> Improved=Yes
- cognitive_complexity: d=0.738 (mediano), p_FDR=5.6e-06, ↔ cambio relativo NA (AP1=139, AP2=505) -> Improved=No
- vulnerabilities: d=-0.718 (mediano), p_FDR=1.9e-05, ↓ cambio relativo NA (AP1=0.55, AP2=0.0833) -> Improved=Yes
- ncloc: d=0.650 (mediano), p_FDR=2.35e-05, ↔ cambio relativo NA (AP1=3.5e+03, AP2=7.28e+03) -> Improved=Neutral
- reliability_rating: d=-0.533 (mediano), p_FDR=0.000638, ↓ cambio relativo NA (AP1=2.27, AP2=1.43) -> Improved=Yes

## Tabla Detallada

|metric|mean_ap1|mean_ap2|pct_change|test_used|p_value|p_value_fdr|effect_size_d|effect_magnitude|improved|
|---|---|---|---|---|---|---|---|---|---|
|cognitive_complexity|139|505|NA|wilcoxon|5.6e-07|5.6e-06|0.738|mediano|No|
|security_rating|2.93|1.23|NA|wilcoxon|3.16e-06|1.58e-05|-0.751|mediano|Yes|
|vulnerabilities|0.55|0.0833|NA|wilcoxon|5.7e-06|1.9e-05|-0.718|mediano|Yes|
|ncloc|3.5e+03|7.28e+03|NA|wilcoxon|9.39e-06|2.35e-05|0.65|mediano|Neutral|
|bugs|4.2|0.467|NA|wilcoxon|6.75e-05|0.000135|-0.523|mediano|Yes|
|reliability_rating|2.27|1.43|NA|wilcoxon|0.000383|0.000638|-0.533|mediano|Yes|
|code_smells|56.9|77.2|NA|wilcoxon|0.051|0.0729|0.255|pequeño|No|
|open_issues|61.6|77.8|NA|wilcoxon|0.13|0.163|0.195|trivial|No|
|security_hotspots|1.53|1.6|NA|wilcoxon|0.256|0.285|0.0335|trivial|No|
|complexity|457|437|NA|paired_t|0.732|0.732|-0.0444|trivial|Yes|

## Interpretación General

Las métricas con mejoras significativas muestran evidencia de impacto positivo (ej. security_rating, vulnerabilities, bugs...).
Atención: algunas métricas empeoraron significativamente (ej. cognitive_complexity).
Los tamaños de efecto clasificados como medianos indican cambios sustanciales prácticos; revisar contexto pedagógico.