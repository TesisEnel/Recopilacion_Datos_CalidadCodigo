# Prompt: Análisis Estadístico - Evolución de Calidad de Código en Estudiantes de Programación Aplicada

**Rol:** Actúa como un estadístico especializado en análisis educativo y métricas de calidad de software, con experiencia en SonarCloud y análisis pre-post intervención.

## **Contexto de la Investigación**

**Investigador:** Enel Almonte  
**Institución:** Universidad Católica Nordestana (UCNE)  
**Tesis:** "Análisis de la Evolución de la Calidad del Código en Estudiantes de Programación Aplicada mediante Métricas de SonarCloud"

### **Objetivo General**
Analizar la evolución de la calidad del código fuente desarrollado por estudiantes de Ingeniería en Sistemas de la UCNE al comparar los proyectos finales de la asignatura Programación Aplicada I y Programación Aplicada II.

### **Objetivos Específicos**
1. **Diagnosticar** la calidad del código (pre-test) de los proyectos finales de Programación Aplicada I
2. **Medir** la calidad del código (post-test) de los proyectos finales de Programación Aplicada II
3. **Determinar** si existe una evolución estadísticamente significativa en la calidad del código entre ambas asignaturas

### **Pregunta de Investigación**
¿Cómo evoluciona la calidad del código fuente producido por estudiantes de Ingeniería en Sistemas de la UCNE al transitar de Programación Aplicada I a Programación Aplicada II?

### **Hipótesis**
- **H₀**: No existe diferencia estadísticamente significativa en las métricas de calidad del código entre AP1 y AP2
- **H₁**: Existe mejora estadísticamente significativa en las métricas de calidad del código de AP1 a AP2

### **Variables**
- **Variable Independiente**: Intervención pedagógica (taller "Código Limpio" en AP2)
- **Variable Dependiente**: Métricas de calidad del código de SonarCloud

---

## **Dataset y Métricas**

### **Datos Disponibles**
- **60 estudiantes** con proyectos en AP1 (pre-test) y AP2 (post-test)
- **14 métricas de SonarCloud** por proyecto
- **Datos demográficos**: género, año académico
- **Diseño**: Pre-test/Post-test con intervención

### **Métricas Principales (Variables de la Tesis)**
**Mantenibilidad:**
- `technical_debt` - Deuda técnica (horas)
- `code_smells` - Código mal olientes
- `duplicated_lines_density` - Porcentaje código duplicado
- `cognitive_complexity` - Complejidad cognitiva

**Fiabilidad:**
- `bugs` - Número de errores
- `reliability_rating` - Calificación fiabilidad (A-E)

**Seguridad:**
- `vulnerabilities` - Vulnerabilidades
- `security_rating` - Calificación seguridad (A-E)

**Métricas Complementarias:**
- `complexity`, `comment_lines_density`, `ncloc`, `security_hotspots`, `sqale_rating`, `open_issues`

### **Archivo de Datos**
```
URL: https://raw.githubusercontent.com/TesisEnel/Recopilacion_Datos_CalidadCodigo/main/data/Estudiantes_2023-2024_con_metricas_sonarcloud.csv
```

---

## **Análisis Estadístico Requerido**

### **1. Análisis Exploratorio de Datos (EDA)**
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import shapiro, wilcoxon, ttest_rel

# Cargar datos
url = 'https://raw.githubusercontent.com/TesisEnel/Recopilacion_Datos_CalidadCodigo/main/data/Estudiantes_2023-2024_con_metricas_sonarcloud.csv'
df = pd.read_csv(url)

# EDA básico
print("Estructura del dataset:")
print(f"Dimensiones: {df.shape}")
print(f"Columnas: {df.columns.tolist()}")
print("\nPrimeras filas:")
df.head()
```

**Análisis descriptivo:**
- Estadísticas descriptivas por asignatura (AP1 vs AP2)
- Distribuciones de cada métrica
- Valores faltantes y outliers
- Correlaciones entre métricas

### **2. Análisis Inferencial Principal**

**Pruebas de normalidad y selección de test:**
```python
def analyze_metric_evolution(df, metric):
    """Analiza la evolución de una métrica entre AP1 y AP2"""
    
    # Datos pareados
    ap1_data = df[df['asignatura'] == 'AP1'][metric]
    ap2_data = df[df['asignatura'] == 'AP2'][metric]
    
    # Verificar si son datos pareados del mismo estudiante
    differences = ap2_data.values - ap1_data.values
    
    # Prueba de normalidad
    _, p_norm = shapiro(differences)
    
    if p_norm > 0.05:
        # Datos normales: T-test pareado
        stat, p_val = ttest_rel(ap1_data, ap2_data)
        test_used = 'T-test pareado'
    else:
        # Datos no normales: Wilcoxon
        stat, p_val = wilcoxon(ap1_data, ap2_data)
        test_used = 'Wilcoxon signed-rank'
    
    # Tamaño del efecto
    cohen_d = (ap2_data.mean() - ap1_data.mean()) / np.sqrt(((ap2_data.std()**2 + ap1_data.std()**2) / 2))
    
    return {
        'metric': metric,
        'test': test_used,
        'statistic': stat,
        'p_value': p_val,
        'cohen_d': cohen_d,
        'ap1_mean': ap1_data.mean(),
        'ap2_mean': ap2_data.mean(),
        'improvement': ap2_data.mean() - ap1_data.mean()
    }
```

### **3. Análisis por Dimensiones de Calidad**
```python
# Agrupar métricas por dimensión
quality_dimensions = {
    'Mantenibilidad': ['technical_debt', 'code_smells', 'duplicated_lines_density', 'cognitive_complexity'],
    'Fiabilidad': ['bugs', 'reliability_rating'],
    'Seguridad': ['vulnerabilities', 'security_rating']
}

# Análisis por dimensión
for dimension, metrics in quality_dimensions.items():
    print(f"\n=== Análisis de {dimension} ===")
    for metric in metrics:
        result = analyze_metric_evolution(df, metric)
        print(f"{metric}: p-value = {result['p_value']:.4f}, Cohen's d = {result['cohen_d']:.3f}")
```

### **4. Corrección por Comparaciones Múltiples**
```python
from statsmodels.stats.multitest import multipletests

# Obtener p-values de todas las métricas
p_values = [analyze_metric_evolution(df, metric)['p_value'] for metric in all_metrics]

# Corrección FDR (Benjamini-Hochberg)
rejected, corrected_p, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

print("Resultados con corrección FDR:")
for i, metric in enumerate(all_metrics):
    print(f"{metric}: p-corregido = {corrected_p[i]:.4f}, Significativo = {rejected[i]}")
```

### **5. Visualizaciones Esenciales**
```python
# Box plots comparativos
fig, axes = plt.subplots(2, 4, figsize=(16, 10))
main_metrics = ['technical_debt', 'code_smells', 'bugs', 'vulnerabilities', 
                'duplicated_lines_density', 'cognitive_complexity', 'reliability_rating', 'security_rating']

for i, metric in enumerate(main_metrics):
    ax = axes[i//4, i%4]
    df.boxplot(column=metric, by='asignatura', ax=ax)
    ax.set_title(f'{metric}')

plt.tight_layout()
plt.show()

# Heatmap de correlaciones
correlation_matrix = df[main_metrics].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Matriz de Correlaciones - Métricas de Calidad')
plt.show()
```

---

## **Entregables**

### **1. Análisis Estadístico Completo**
- Notebook con código ejecutable y resultados
- Interpretación de cada prueba estadística
- Tablas de resultados con p-values y tamaños del efecto

### **2. Resumen de Resultados**
- Tabla resumen con todas las métricas analizadas
- Identificación de mejoras estadísticamente significativas
- Magnitud de las mejoras (tamaño del efecto)

### **3. Visualizaciones**
- Box plots comparativos AP1 vs AP2
- Gráficos de evolución individual por estudiante
- Heatmap de correlaciones entre métricas

### **4. Conclusiones Estadísticas**
- Respuesta a la hipótesis principal
- Interpretación práctica de los resultados
- Limitaciones del análisis

---

## **Consideraciones Metodológicas**

- **Diseño**: Pre-test/Post-test pareado
- **Nivel de significancia**: α = 0.05
- **Corrección**: FDR para comparaciones múltiples
- **Tamaño del efecto**: Cohen's d para interpretación práctica
- **Supuestos**: Verificación de normalidad para selección de pruebas apropiadas

**Enfoque**: Análisis riguroso pero conciso, enfocado en responder la pregunta de investigación central sin elementos innecesarios para una tesis académica.
