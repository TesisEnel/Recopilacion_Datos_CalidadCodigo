# Informe Formal de Resultados Estadísticos

## 1. Introducción
Análisis pareado AP1 vs AP2 de métricas SonarCloud.
## 2. Metodología
Pruebas t pareada o Wilcoxon; FDR Benjamini-Hochberg; d de Cohen pareado.
## 3. Resultados Globales
Se evaluaron 10 métricas; 6 significativas (FDR≤0.05).
Mejoras: security_rating, vulnerabilities, bugs, reliability_rating.
Deterioros: cognitive_complexity.
Neutrales/contexto: ncloc.
## 4. Tabla Resumida (principales métricas)
|metric|mean_ap1|mean_ap2|pct_change|p_value_fdr|effect_size_d|effect_magnitude|improved|
|---|---|---|---|---|---|---|---|
|cognitive_complexity|139|505|<bound method NDFrame.pct_change of metric              cognitive_complexity
mean_ap1                      139.033333
mean_ap2                      505.283333
pct_change                        263.4%
p_value_fdr                     0.000006
effect_size_d                   0.738322
effect_magnitude                 mediano
improved                              No
Name: 4, dtype: object>|5.6e-06|0.738|mediano|No|
|security_rating|2.93|1.23|<bound method NDFrame.pct_change of metric              security_rating
mean_ap1                   2.933333
mean_ap2                   1.233333
pct_change                   -58.0%
p_value_fdr                0.000016
effect_size_d             -0.750655
effect_magnitude            mediano
improved                        Yes
Name: 8, dtype: object>|1.58e-05|-0.751|mediano|Yes|
|vulnerabilities|0.55|0.0833|<bound method NDFrame.pct_change of metric              vulnerabilities
mean_ap1                       0.55
mean_ap2                   0.083333
pct_change                   -84.8%
p_value_fdr                0.000019
effect_size_d             -0.717865
effect_magnitude            mediano
improved                        Yes
Name: 2, dtype: object>|1.9e-05|-0.718|mediano|Yes|
|ncloc|3.5e+03|7.28e+03|<bound method NDFrame.pct_change of metric                    ncloc
mean_ap1            3499.766667
mean_ap2                7281.85
pct_change               108.1%
p_value_fdr            0.000023
effect_size_d          0.649901
effect_magnitude        mediano
improved                Neutral
Name: 6, dtype: object>|2.35e-05|0.65|mediano|Neutral|
|bugs|4.2|0.467|<bound method NDFrame.pct_change of metric                  bugs
mean_ap1                 4.2
mean_ap2            0.466667
pct_change            -88.9%
p_value_fdr         0.000135
effect_size_d      -0.522881
effect_magnitude     mediano
improved                 Yes
Name: 1, dtype: object>|0.000135|-0.523|mediano|Yes|
|reliability_rating|2.27|1.43|<bound method NDFrame.pct_change of metric              reliability_rating
mean_ap1                      2.266667
mean_ap2                      1.433333
pct_change                      -36.8%
p_value_fdr                   0.000638
effect_size_d                -0.532797
effect_magnitude               mediano
improved                           Yes
Name: 7, dtype: object>|0.000638|-0.533|mediano|Yes|
|code_smells|56.9|77.2|<bound method NDFrame.pct_change of metric              code_smells
mean_ap1                  56.85
mean_ap2              77.233333
pct_change                35.9%
p_value_fdr            0.072882
effect_size_d          0.254705
effect_magnitude        pequeño
improved                     No
Name: 0, dtype: object>|0.0729|0.255|pequeño|No|
|open_issues|61.6|77.8|<bound method NDFrame.pct_change of metric              open_issues
mean_ap1                   61.6
mean_ap2              77.783333
pct_change                26.3%
p_value_fdr            0.162664
effect_size_d          0.195296
effect_magnitude        trivial
improved                     No
Name: 9, dtype: object>|0.163|0.195|trivial|No|
|security_hotspots|1.53|1.6|<bound method NDFrame.pct_change of metric              security_hotspots
mean_ap1                     1.533333
mean_ap2                          1.6
pct_change                       4.3%
p_value_fdr                  0.284553
effect_size_d                0.033495
effect_magnitude              trivial
improved                           No
Name: 3, dtype: object>|0.285|0.0335|trivial|No|
|complexity|457|437|<bound method NDFrame.pct_change of metric              complexity
mean_ap1            456.783333
mean_ap2            436.616667
pct_change               -4.4%
p_value_fdr           0.732304
effect_size_d         -0.04437
effect_magnitude       trivial
improved                   Yes
Name: 5, dtype: object>|0.732|-0.0444|trivial|Yes|
## 5. Gráficos
![fig_boxplots.png](fig_boxplots.png)
![fig_heatmap_correlaciones.png](fig_heatmap_correlaciones.png)

## 6. Conclusiones
Mejoras en defectos y seguridad; pendiente refactorización para complejidad y duplicación.