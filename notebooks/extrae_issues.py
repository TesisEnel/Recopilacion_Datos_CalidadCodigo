# %% [markdown]
# # Extracción Simplificada de Issues desde SonarCloud
# 
# Este notebook te permite extraer todos los issues de un proyecto específico de SonarCloud utilizando únicamente el ProjectKey.
# 
# ## Características:
# - **Entrada simple**: Solo necesitas el ProjectKey del proyecto
# - **Extracción completa**: Obtiene todos los issues del proyecto
# - **Agrupación automática**: Presenta los issues organizados por categorías
# - **Visualización clara**: Muestra los resultados de forma fácil de entender
# 
# ## ¿Qué información obtienes?
# - Issues agrupados por severidad (CRITICAL, MAJOR, MINOR, etc.)
# - Issues agrupados por tipo (BUG, VULNERABILITY, CODE_SMELL)
# - Issues agrupados por regla aplicada
# - Detalles de cada issue incluyendo archivo y línea afectada

# %%
# Importar librerías necesarias
import requests
import pandas as pd
import json
from collections import defaultdict
import time

print("✅ Librerías importadas correctamente")

# %%
# Configuración de SonarCloud
SONARCLOUD_BASE_URL = "https://sonarcloud.io/api"
ISSUES_ENDPOINT = f"{SONARCLOUD_BASE_URL}/issues/search"

def extraer_issues_proyecto(project_key, max_issues=10000):
    """
    Extrae todos los issues de un proyecto de SonarCloud
    
    Args:
        project_key (str): Clave del proyecto en SonarCloud
        max_issues (int): Número máximo de issues a extraer
    
    Returns:
        list: Lista de issues extraídos
    """
    all_issues = []
    page = 1
    page_size = 500  # Máximo permitido por SonarCloud
    
    print(f"🔍 Extrayendo issues del proyecto: {project_key}")
    
    while len(all_issues) < max_issues:
        params = {
            'componentKeys': project_key,
            'p': page,
            'ps': page_size,
            'resolved': 'false'  # Solo issues no resueltos
        }
        
        try:
            response = requests.get(ISSUES_ENDPOINT, params=params)
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                
                if not issues:
                    break
                
                all_issues.extend(issues)
                print(f"📄 Página {page}: {len(issues)} issues extraídos (Total: {len(all_issues)})")
                
                # Verificar si hay más páginas
                total_issues = data.get('total', 0)
                if len(all_issues) >= total_issues:
                    break
                
                page += 1
                time.sleep(0.5)  # Pausa para evitar rate limiting
                
            elif response.status_code == 404:
                print(f"❌ Proyecto no encontrado: {project_key}")
                break
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                break
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            break
    
    print(f"✅ Extracción completada: {len(all_issues)} issues totales")
    return all_issues

print("✅ Función de extracción definida")

# %%
def procesar_y_agrupar_issues(issues_data):
    """
    Procesa y agrupa los issues extraídos
    
    Args:
        issues_data (list): Lista de issues de SonarCloud
    
    Returns:
        dict: Diccionario con issues agrupados por diferentes categorías
    """
    if not issues_data:
        return {}
    
    # Crear agrupaciones
    agrupaciones = {
        'por_severidad': defaultdict(list),
        'por_tipo': defaultdict(list),
        'por_regla': defaultdict(list),
        'por_archivo': defaultdict(list)
    }
    
    for issue in issues_data:
        # Información básica del issue
        issue_info = {
            'key': issue.get('key', ''),
            'message': issue.get('message', ''),
            'severity': issue.get('severity', 'UNKNOWN'),
            'type': issue.get('type', 'UNKNOWN'),
            'rule': issue.get('rule', 'UNKNOWN'),
            'component': issue.get('component', ''),
            'line': issue.get('line', 'N/A'),
            'status': issue.get('status', 'UNKNOWN')
        }
        
        # Agrupar por severidad
        agrupaciones['por_severidad'][issue_info['severity']].append(issue_info)
        
        # Agrupar por tipo
        agrupaciones['por_tipo'][issue_info['type']].append(issue_info)
        
        # Agrupar por regla
        agrupaciones['por_regla'][issue_info['rule']].append(issue_info)
        
        # Agrupar por archivo
        archivo = issue_info['component'].split(':')[-1] if ':' in issue_info['component'] else issue_info['component']
        agrupaciones['por_archivo'][archivo].append(issue_info)
    
    return agrupaciones

def mostrar_resumen_agrupaciones(agrupaciones):
    """
    Muestra un resumen de las agrupaciones de issues
    """
    if not agrupaciones:
        print("❌ No hay issues para mostrar")
        return
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE ISSUES AGRUPADOS")
    print("="*60)
    
    # Resumen por severidad
    print("\n🔥 ISSUES POR SEVERIDAD:")
    for severidad, issues in sorted(agrupaciones['por_severidad'].items()):
        print(f"  • {severidad}: {len(issues)} issues")
    
    # Resumen por tipo
    print("\n🏷️ ISSUES POR TIPO:")
    for tipo, issues in sorted(agrupaciones['por_tipo'].items()):
        print(f"  • {tipo}: {len(issues)} issues")
    
    # Top 10 reglas más frecuentes
    print("\n📜 TOP 10 REGLAS MÁS FRECUENTES:")
    reglas_ordenadas = sorted(agrupaciones['por_regla'].items(), key=lambda x: len(x[1]), reverse=True)
    for i, (regla, issues) in enumerate(reglas_ordenadas[:10], 1):
        print(f"  {i:2d}. {regla}: {len(issues)} issues")
    
    # Top 10 archivos más problemáticos
    print("\n📁 TOP 10 ARCHIVOS MÁS PROBLEMÁTICOS:")
    archivos_ordenados = sorted(agrupaciones['por_archivo'].items(), key=lambda x: len(x[1]), reverse=True)
    for i, (archivo, issues) in enumerate(archivos_ordenados[:10], 1):
        print(f"  {i:2d}. {archivo}: {len(issues)} issues")

print("✅ Funciones de procesamiento y visualización definidas")

# %%
def mostrar_detalles_agrupacion(agrupaciones, tipo_agrupacion, nombre_grupo, max_issues=10):
    """
    Muestra los detalles de un grupo específico de issues
    
    Args:
        agrupaciones (dict): Diccionario con agrupaciones
        tipo_agrupacion (str): Tipo de agrupación ('por_severidad', 'por_tipo', etc.)
        nombre_grupo (str): Nombre del grupo específico
        max_issues (int): Número máximo de issues a mostrar
    """
    if tipo_agrupacion not in agrupaciones:
        print(f"❌ Tipo de agrupación '{tipo_agrupacion}' no encontrado")
        return
    
    if nombre_grupo not in agrupaciones[tipo_agrupacion]:
        print(f"❌ Grupo '{nombre_grupo}' no encontrado en '{tipo_agrupacion}'")
        print(f"Grupos disponibles: {list(agrupaciones[tipo_agrupacion].keys())}")
        return
    
    issues = agrupaciones[tipo_agrupacion][nombre_grupo]
    total_issues = len(issues)
    
    print(f"\n{'='*80}")
    print(f"📋 DETALLES - {tipo_agrupacion.replace('_', ' ').upper()}: {nombre_grupo}")
    print(f"Total de issues: {total_issues}")
    print(f"Mostrando: {min(max_issues, total_issues)} issues")
    print(f"{'='*80}")
    
    for i, issue in enumerate(issues[:max_issues], 1):
        print(f"\n{i:2d}. 🔍 Issue: {issue['key']}")
        print(f"    📝 Mensaje: {issue['message']}")
        print(f"    🔥 Severidad: {issue['severity']}")
        print(f"    🏷️  Tipo: {issue['type']}")
        print(f"    📜 Regla: {issue['rule']}")
        print(f"    📁 Archivo: {issue['component'].split(':')[-1] if ':' in issue['component'] else issue['component']}")
        print(f"    📍 Línea: {issue['line']}")
        print(f"    ⏸️  Estado: {issue['status']}")
    
    if total_issues > max_issues:
        print(f"\n... y {total_issues - max_issues} issues más")

print("✅ Función de detalles definida")

# %% [markdown]
# ## 🚀 Extracción de Issues
# 
# **Instrucciones:**
# 1. Ejecuta la celda siguiente
# 2. Ingresa el ProjectKey cuando se te solicite
# 3. Espera a que se complete la extracción
# 4. Revisa los resultados agrupados

# %%
# 🎯 EXTRACCIÓN PRINCIPAL
# Solicitar ProjectKey al usuario
project_key = input("🔑 Ingresa el ProjectKey del proyecto de SonarCloud: ").strip()

if not project_key:
    print("❌ ProjectKey no puede estar vacío")
else:
    print(f"\n🚀 Iniciando extracción para el proyecto: {project_key}")
    print("-" * 60)
    
    # Extraer issues
    issues_extraidos = extraer_issues_proyecto(project_key)
    
        # Crear DataFrame
    df_issues = pd.DataFrame(issues_extraidos)
    
    # Nombre del archivo
    nombre_archivo = f"General_issues_10.csv"
    
    # Guardar archivo
    df_issues.to_csv(nombre_archivo, index=False, encoding='utf-8')

    if issues_extraidos:
        # Procesar y agrupar
        agrupaciones = procesar_y_agrupar_issues(issues_extraidos)
        
        # Mostrar resumen
        mostrar_resumen_agrupaciones(agrupaciones)
        
        print(f"\n✅ Extracción completada exitosamente!")
        print(f"📊 Total de issues extraídos: {len(issues_extraidos)}")
        
        # Guardar variables para uso posterior
        globals()['ultimo_project_key'] = project_key
        globals()['ultimos_issues'] = issues_extraidos
        globals()['ultimas_agrupaciones'] = agrupaciones
        
    else:
        print("❌ No se pudieron extraer issues. Verifica el ProjectKey y tu conexión.")

# %% [markdown]
# ## 🔍 Exploración Detallada
# 
# Usa las siguientes celdas para explorar los issues en detalle:

# %%
# 📋 EXPLORAR ISSUES POR SEVERIDAD
# Ejecuta esta celda para ver los issues de una severidad específica

if 'ultimas_agrupaciones' in globals():
    print("🔥 Severidades disponibles:")
    for severidad in sorted(ultimas_agrupaciones['por_severidad'].keys()):
        count = len(ultimas_agrupaciones['por_severidad'][severidad])
        print(f"  • {severidad} ({count} issues)")
    
    print("\n💡 Para ver detalles, ejecuta la siguiente línea cambiando 'MAJOR' por la severidad deseada:")
    print("mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_severidad', 'MAJOR', 5)")
    
    # Ejemplo: mostrar issues CRITICAL (si existen)
    if 'CRITICAL' in ultimas_agrupaciones['por_severidad']:
        print("\n🚨 Mostrando issues CRITICAL como ejemplo:")
        mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_severidad', 'CRITICAL', 100)
else:
    print("❌ Primero debes extraer issues ejecutando la celda de extracción")

# %%
# 🏷️ EXPLORAR ISSUES POR TIPO
# Ejecuta esta celda para ver los issues de un tipo específico

if 'ultimas_agrupaciones' in globals():
    print("🏷️ Tipos disponibles:")
    for tipo in sorted(ultimas_agrupaciones['por_tipo'].keys()):
        count = len(ultimas_agrupaciones['por_tipo'][tipo])
        print(f"  • {tipo} ({count} issues)")
    
    print("\n💡 Para ver detalles, ejecuta la siguiente línea cambiando 'CODE_SMELL' por el tipo deseado:")
    print("mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_tipo', 'CODE_SMELL', 5)")
    
    # Ejemplo: mostrar issues de BUGS (si existen)
    if 'BUG' in ultimas_agrupaciones['por_tipo']:
        print("\n🐛 Mostrando BUGS como ejemplo:")
        mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_tipo', 'BUG', 3)
else:
    print("❌ Primero debes extraer issues ejecutando la celda de extracción")

# %%
# 📜 EXPLORAR ISSUES POR REGLA ESPECÍFICA
# Ejecuta esta celda para ver los issues de una regla específica

if 'ultimas_agrupaciones' in globals():
    print("📜 Top 15 reglas más frecuentes:")
    reglas_ordenadas = sorted(ultimas_agrupaciones['por_regla'].items(), 
                             key=lambda x: len(x[1]), reverse=True)
    
    for i, (regla, issues) in enumerate(reglas_ordenadas[:150], 1):
        print(f"  {i:2d}. {regla} ({len(issues)} issues)")
    
    print("\n💡 Para ver detalles de una regla específica, copia el nombre de la regla y ejecuta:")
    print("mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_regla', 'NOMBRE_DE_LA_REGLA', 5)")
    
    # Ejemplo: mostrar la regla más frecuente
    if reglas_ordenadas:
        regla_mas_frecuente = reglas_ordenadas[0][0]
        print(f"\n📍 Mostrando ejemplos de la regla más frecuente: {regla_mas_frecuente}")
        mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_regla', regla_mas_frecuente, 3)
else:
    print("❌ Primero debes extraer issues ejecutando la celda de extracción")

# %%
# 📁 EXPLORAR ISSUES POR ARCHIVO
# Ejecuta esta celda para ver los archivos más problemáticos

if 'ultimas_agrupaciones' in globals():
    print("📁 Top 15 archivos más problemáticos:")
    archivos_ordenados = sorted(ultimas_agrupaciones['por_archivo'].items(), 
                               key=lambda x: len(x[1]), reverse=True)
    
    for i, (archivo, issues) in enumerate(archivos_ordenados[:150], 1):
        print(f"  {i:2d}. {archivo} ({len(issues)} issues)")
    
    print("\n💡 Para ver detalles de un archivo específico, copia el nombre del archivo y ejecuta:")
    print("mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_archivo', 'NOMBRE_DEL_ARCHIVO', 5)")
    
    # Ejemplo: mostrar el archivo más problemático
    if archivos_ordenados:
        archivo_mas_problematico = archivos_ordenados[0][0]
        print(f"\n📍 Mostrando issues del archivo más problemático: {archivo_mas_problematico}")
        mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_archivo', archivo_mas_problematico, 3)
else:
    print("❌ Primero debes extraer issues ejecutando la celda de extracción")

# %% [markdown]
# ## 💾 Exportar Resultados
# 
# Ejecuta la siguiente celda para guardar los resultados en un archivo CSV:

# %%
# 💾 EXPORTAR RESULTADOS A CSV

if 'ultimos_issues' in globals() and 'ultimo_project_key' in globals():
    # Convertir issues a DataFrame
    issues_para_csv = []
    
    for issue in ultimos_issues:
        issue_data = {
            'project_key': ultimo_project_key,
            'issue_key': issue.get('key', ''),
            'message': issue.get('message', ''),
            'severity': issue.get('severity', ''),
            'type': issue.get('type', ''),
            'rule': issue.get('rule', ''),
            'component': issue.get('component', ''),
            'line': issue.get('line', ''),
            'status': issue.get('status', ''),
            'creation_date': issue.get('creationDate', ''),
            'update_date': issue.get('updateDate', '')
        }
        issues_para_csv.append(issue_data)
    
    # Crear DataFrame
    df_issues = pd.DataFrame(issues_para_csv)
    
    # Nombre del archivo
    nombre_archivo = f"issues_{ultimo_project_key.replace(':', '_')}.csv"
    
    # Guardar archivo
    df_issues.to_csv(nombre_archivo, index=False, encoding='utf-8')
    
    print(f"✅ Resultados exportados exitosamente a: {nombre_archivo}")
    print(f"📊 Registros exportados: {len(df_issues)}")
    print(f"📋 Columnas: {list(df_issues.columns)}")
    
    # Mostrar preview
    print("\n👀 Vista previa del archivo:")
    print(df_issues.head())
    
else:
    print("❌ No hay datos para exportar. Primero extrae issues ejecutando la celda de extracción.")

# %% [markdown]
# ## 📖 Guía de Uso
# 
# ### Pasos para usar este notebook:
# 
# 1. **Ejecuta todas las celdas de configuración** (las primeras 4 celdas con código)
# 2. **Ejecuta la celda de extracción principal** e ingresa tu ProjectKey
# 3. **Revisa el resumen automático** que se muestra
# 4. **Explora en detalle** usando las celdas de exploración
# 5. **Exporta los resultados** si necesitas un archivo CSV
# 
# ### Ejemplos de ProjectKeys:
# - `organization_project-name`
# - `user_repository-name`
# - `company_application-backend`
# 
# ### Comandos útiles para exploración:
# ```python
# # Ver detalles de issues críticos
# mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_severidad', 'CRITICAL', 10)
# 
# # Ver bugs específicos
# mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_tipo', 'BUG', 5)
# 
# # Ver issues de una regla específica
# mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_regla', 'java:S1481', 5)
# 
# # Ver issues de un archivo específico
# mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_archivo', 'Main.java', 10)
# ```

# %%
# 💾 EXPORTAR RESULTADOS A CSV
mostrar_detalles_agrupacion(ultimas_agrupaciones, 'por_severidad', 'MAJOR', 5)