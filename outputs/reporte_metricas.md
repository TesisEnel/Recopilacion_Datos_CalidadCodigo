# Reporte Estadístico de Métricas AP1 vs AP2

Generado: 2025-08-09 10:42

Fuente CSV: `data/Estudiantes_2023-2024_con_metricas_sonarcloud.csv`

## Resumen Global

Se analizaron 15 métricas. 8 resultaron significativas tras corrección FDR (α=0.05).

- Mejoras significativas: 4 -> bugs, security_rating, reliability_rating, vulnerabilities
- Deterioros significativos: 3 -> duplicated_lines_density, cognitive_complexity, comment_lines_density
- Cambios significativos pero neutros (contexto): 1 -> ncloc

## Principales Cambios (Top |d|)

- security_rating: d=-0.751 (mediano), p_FDR=1.22e-05, ↓ cambio relativo NA (AP1=2.93, AP2=1.23) -> Improved=Yes
- reliability_rating: d=-0.743 (mediano), p_FDR=1.34e-05, ↓ cambio relativo NA (AP1=2.27, AP2=1.17) -> Improved=Yes
- vulnerabilities: d=-0.718 (mediano), p_FDR=1.34e-05, ↓ cambio relativo NA (AP1=0.55, AP2=0.0833) -> Improved=Yes
- cognitive_complexity: d=0.703 (mediano), p_FDR=1.22e-05, ↔ cambio relativo NA (AP1=139, AP2=414) -> Improved=No
- duplicated_lines_density: d=0.602 (mediano), p_FDR=1.22e-05, ↔ cambio relativo NA (AP1=1.62, AP2=6.73) -> Improved=No

## Tabla Detallada

|metric|mean_ap1|mean_ap2|pct_change|test_used|p_value|p_value_fdr|effect_size_d|effect_magnitude|improved|
|---|---|---|---|---|---|---|---|---|---|
|bugs|4.2|0.2|NA|wilcoxon|4.07e-06|1.22e-05|-0.566|mediano|Yes|
|duplicated_lines_density|1.62|6.73|NA|wilcoxon|2.02e-06|1.22e-05|0.602|mediano|No|
|cognitive_complexity|139|414|NA|wilcoxon|3.64e-06|1.22e-05|0.703|mediano|No|
|security_rating|2.93|1.23|NA|wilcoxon|3.16e-06|1.22e-05|-0.751|mediano|Yes|
|reliability_rating|2.27|1.17|NA|wilcoxon|6.68e-06|1.34e-05|-0.743|mediano|Yes|
|vulnerabilities|0.55|0.0833|NA|wilcoxon|5.7e-06|1.34e-05|-0.718|mediano|Yes|
|ncloc|3.5e+03|6.13e+03|NA|paired_t|7.23e-05|0.000124|0.551|mediano|Neutral|
|comment_lines_density|3.44|2.6|NA|wilcoxon|0.00483|0.00724|-0.231|pequeño|No|
|complexity|457|371|NA|paired_t|0.115|0.153|-0.207|pequeño|Yes|
|code_smells|56.9|67|NA|wilcoxon|0.213|0.256|0.145|trivial|No|
|open_issues|61.6|67.3|NA|wilcoxon|0.455|0.496|0.0784|trivial|No|
|security_hotspots|1.53|1.45|NA|wilcoxon|0.648|0.648|-0.0423|trivial|Yes|
|technical_debt|NA|NA|NA|Insuficiente|NA|NA|NA|lower_better|NA|
|coverage|NA|NA|NA|Insuficiente|NA|NA|NA|higher_better|NA|
|sqale_rating|1|1|NA|paired_t|NA|NA|0|trivial|No|

## Interpretación General

Las métricas con mejoras significativas muestran evidencia de impacto positivo (ej. bugs, security_rating, reliability_rating...).
Atención: algunas métricas empeoraron significativamente (ej. duplicated_lines_density, cognitive_complexity, comment_lines_density).
Los tamaños de efecto clasificados como medianos indican cambios sustanciales prácticos; revisar contexto pedagógico.