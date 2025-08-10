# Informe Formal de Resultados Estadísticos

## 1. Introducción
Análisis pareado AP1 vs AP2 de métricas SonarCloud.
## 2. Metodología
Pruebas t pareada o Wilcoxon; FDR Benjamini-Hochberg; d de Cohen pareado.
## 3. Resultados Globales
Se evaluaron 15 métricas; 8 significativas (FDR≤0.05).
Mejoras: bugs, security_rating, reliability_rating, vulnerabilities.
Deterioros: duplicated_lines_density, cognitive_complexity, comment_lines_density.
Neutrales/contexto: ncloc.
## 4. Tabla Resumida (principales métricas)
|metric|mean_ap1|mean_ap2|pct_change|p_value_fdr|effect_size_d|effect_magnitude|improved|
|---|---|---|---|---|---|---|---|
|bugs|4.2|0.2|<bound method NDFrame.pct_change of metric                  bugs
mean_ap1                 4.2
mean_ap2                 0.2
pct_change            -95.2%
p_value_fdr         0.000012
effect_size_d      -0.566069
effect_magnitude     mediano
improved                 Yes
Name: 2, dtype: object>|1.22e-05|-0.566|mediano|Yes|
|duplicated_lines_density|1.62|6.73|<bound method NDFrame.pct_change of metric              duplicated_lines_density
mean_ap1                            1.623333
mean_ap2                               6.735
pct_change                            314.9%
p_value_fdr                         0.000012
effect_size_d                       0.602267
effect_magnitude                     mediano
improved                                  No
Name: 5, dtype: object>|1.22e-05|0.602|mediano|No|
|cognitive_complexity|139|414|<bound method NDFrame.pct_change of metric              cognitive_complexity
mean_ap1                      139.033333
mean_ap2                      413.933333
pct_change                        197.7%
p_value_fdr                     0.000012
effect_size_d                   0.703004
effect_magnitude                 mediano
improved                              No
Name: 6, dtype: object>|1.22e-05|0.703|mediano|No|
|security_rating|2.93|1.23|<bound method NDFrame.pct_change of metric              security_rating
mean_ap1                   2.933333
mean_ap2                   1.233333
pct_change                   -58.0%
p_value_fdr                0.000012
effect_size_d             -0.750655
effect_magnitude            mediano
improved                        Yes
Name: 12, dtype: object>|1.22e-05|-0.751|mediano|Yes|
|reliability_rating|2.27|1.17|<bound method NDFrame.pct_change of metric              reliability_rating
mean_ap1                      2.266667
mean_ap2                      1.166667
pct_change                      -48.5%
p_value_fdr                   0.000013
effect_size_d                -0.742765
effect_magnitude               mediano
improved                           Yes
Name: 11, dtype: object>|1.34e-05|-0.743|mediano|Yes|
|vulnerabilities|0.55|0.0833|<bound method NDFrame.pct_change of metric              vulnerabilities
mean_ap1                       0.55
mean_ap2                   0.083333
pct_change                   -84.8%
p_value_fdr                0.000013
effect_size_d             -0.717865
effect_magnitude            mediano
improved                        Yes
Name: 3, dtype: object>|1.34e-05|-0.718|mediano|Yes|
|ncloc|3.5e+03|6.13e+03|<bound method NDFrame.pct_change of metric                    ncloc
mean_ap1            3499.766667
mean_ap2            6134.283333
pct_change                75.3%
p_value_fdr            0.000124
effect_size_d          0.551121
effect_magnitude        mediano
improved                Neutral
Name: 10, dtype: object>|0.000124|0.551|mediano|Neutral|
|comment_lines_density|3.44|2.6|<bound method NDFrame.pct_change of metric              comment_lines_density
mean_ap1                         3.443333
mean_ap2                         2.598333
pct_change                         -24.5%
p_value_fdr                      0.007238
effect_size_d                   -0.231116
effect_magnitude                  pequeño
improved                               No
Name: 9, dtype: object>|0.00724|-0.231|pequeño|No|
|complexity|457|371|<bound method NDFrame.pct_change of metric              complexity
mean_ap1            456.783333
mean_ap2            371.066667
pct_change              -18.8%
p_value_fdr           0.152932
effect_size_d        -0.206699
effect_magnitude       pequeño
improved                   Yes
Name: 7, dtype: object>|0.153|-0.207|pequeño|Yes|
|code_smells|56.9|67|<bound method NDFrame.pct_change of metric              code_smells
mean_ap1                  56.85
mean_ap2                  67.05
pct_change                17.9%
p_value_fdr            0.255514
effect_size_d           0.14471
effect_magnitude        trivial
improved                     No
Name: 1, dtype: object>|0.256|0.145|trivial|No|
|open_issues|61.6|67.3|<bound method NDFrame.pct_change of metric              open_issues
mean_ap1                   61.6
mean_ap2              67.333333
pct_change                 9.3%
p_value_fdr            0.496202
effect_size_d          0.078402
effect_magnitude        trivial
improved                     No
Name: 14, dtype: object>|0.496|0.0784|trivial|No|
|security_hotspots|1.53|1.45|<bound method NDFrame.pct_change of metric              security_hotspots
mean_ap1                     1.533333
mean_ap2                         1.45
pct_change                      -5.4%
p_value_fdr                  0.647844
effect_size_d               -0.042337
effect_magnitude              trivial
improved                          Yes
Name: 4, dtype: object>|0.648|-0.0423|trivial|Yes|
|technical_debt|NA|NA|<bound method NDFrame.pct_change of metric              technical_debt
mean_ap1                       NaN
mean_ap2                       NaN
pct_change                      NA
p_value_fdr                    NaN
effect_size_d                  NaN
effect_magnitude      lower_better
improved                      None
Name: 0, dtype: object>|NA|NA|lower_better|NA|
|coverage|NA|NA|<bound method NDFrame.pct_change of metric                   coverage
mean_ap1                      NaN
mean_ap2                      NaN
pct_change                     NA
p_value_fdr                   NaN
effect_size_d                 NaN
effect_magnitude    higher_better
improved                     None
Name: 8, dtype: object>|NA|NA|higher_better|NA|
|sqale_rating|1|1|<bound method NDFrame.pct_change of metric              sqale_rating
mean_ap1                     1.0
mean_ap2                     1.0
pct_change                  0.0%
p_value_fdr                  NaN
effect_size_d                0.0
effect_magnitude         trivial
improved                      No
Name: 13, dtype: object>|NA|0|trivial|No|
## 5. Gráficos
![fig_boxplots.png](fig_boxplots.png)
![fig_heatmap_correlaciones.png](fig_heatmap_correlaciones.png)

## 6. Conclusiones
Mejoras en defectos y seguridad; pendiente refactorización para complejidad y duplicación.